import httpx
import time
import httpx
from typing import Optional
from config import DEXSCREENER_BASE_URL, ENABLE_TOKEN_BOOSTS, BOOST_COOLDOWN_SEC
from config import SCAN_INTERVAL


class DexScreenerClient:
    def __init__(self):
        self.base_url = DEXSCREENER_BASE_URL
        self.client = httpx.Client(timeout=30.0)
        self.boosts_enabled = ENABLE_TOKEN_BOOSTS
        self._boost_off_until = 0

    def _request(self, endpoint: str) -> Optional[dict]:
        url = f"{self.base_url}{endpoint}"
        try:
            response = self.client.get(url)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"DexScreener API error: {e}")
            # If rate limited, back off boosts as a side effect
            if isinstance(e, httpx.HTTPStatusError) and e.response is not None and e.response.status_code == 429:
                self._boost_off_until = int(time.time()) + BOOST_COOLDOWN_SEC
            return None

    def get_token_pairs(self, chain: str, token_address: str) -> list:
        data = self._request(f"/token-pairs/v1/{chain}/{token_address}")
        if data:
            return data if isinstance(data, list) else [data]
        return []

    def get_boosted_tokens(self) -> list:
        import time
        if not self.boosts_enabled:
            return []
        if int(time.time()) < self._boost_off_until:
            return []
        data = self._request("/token-boosts/latest/v1")
        if data and isinstance(data, list):
            return data
        # If anything goes wrong, back off boosts for a cooldown
        self._boost_off_until = int(time.time()) + BOOST_COOLDOWN_SEC
        return []

    def get_community_takeovers(self) -> list:
        data = self._request("/community-takeovers/latest/v1")
        if data and isinstance(data, list):
            return data
        return []

    def get_volume_spike_tokens(self, min_volume: float = 5000, limit: int = 30) -> list:
        boosted_tokens = self.get_boosted_tokens()
        takeover_tokens = self.get_community_takeovers()
        
        token_addresses = set()
        
        for token in boosted_tokens[:50]:
            addr = token.get("tokenAddress")
            if addr:
                token_addresses.add(addr)
        
        for token in takeover_tokens[:50]:
            addr = token.get("tokenAddress")
            if addr:
                token_addresses.add(addr)
        
        print(f"[DexScreener] Checking {len(token_addresses)} active tokens...")
        
        results = []
        for address in list(token_addresses)[:limit]:
            pairs = self.get_token_pairs("solana", address)
            if not pairs:
                continue
            
            main_pair = pairs[0]
            
            base_token = main_pair.get("baseToken", {})
            mc = main_pair.get("marketCap", 0) or 0
            liquidity = main_pair.get("liquidity", {}).get("usd", 0) or 0
            volume_h24 = main_pair.get("volume", {}).get("h24", 0) or 0
            volume_h1 = main_pair.get("volume", {}).get("h1", 0) or 0
            volume_m5 = main_pair.get("volume", {}).get("m5", 0) or 0
            price_usd = main_pair.get("priceUsd", 0) or 0
            price_change_m5 = main_pair.get("priceChange", {}).get("m5", 0) or 0
            price_change_h1 = main_pair.get("priceChange", {}).get("h1", 0) or 0
            price_change_h24 = main_pair.get("priceChange", {}).get("h24", 0) or 0
            txns_m5 = main_pair.get("txns", {}).get("m5", {}) or {}
            buys_m5 = txns_m5.get("buys", 0) or 0
            sells_m5 = txns_m5.get("sells", 0) or 0
            created_at = main_pair.get("pairCreatedAt", 0) or 0
            
            if mc < 5000:
                continue
            
            results.append({
                "address": address,
                "symbol": base_token.get("symbol", "?"),
                "name": base_token.get("name", "Unknown"),
                "market_cap": mc,
                "liquidity": liquidity,
                "volume_24h": volume_h24,
                "volume_1h": volume_h1,
                "volume_5m": volume_m5,
                "price_usd": price_usd,
                "price_change_m5": price_change_m5,
                "price_change_1h": price_change_h1,
                "price_change_24h": price_change_h24,
                "buys_5m": buys_m5,
                "sells_5m": sells_m5,
                "created_at": created_at,
                "pair_address": main_pair.get("pairAddress", "")
            })
        
        results.sort(key=lambda x: x["volume_5m"], reverse=True)
        return results

    def check_token_age(self, token_address: str) -> tuple[bool, int]:
        pairs = self.get_token_pairs("solana", token_address)
        if not pairs:
            return False, 0
        
        oldest_timestamp = min(p.get("pairCreatedAt", 0) or 0 for p in pairs)
        
        if not oldest_timestamp:
            return False, 0
        
        return True, oldest_timestamp

    def close(self):
        self.client.close()


def get_dexscreener_client() -> DexScreenerClient:
    return DexScreenerClient()
