import time
from datetime import datetime, timedelta
from typing import List
from dexscreener_client import DexScreenerClient
from rugcheck_client import RugCheckClient
from config import (
    MIN_AGE_DAYS,
    MIN_MARKET_CAP,
    MAX_MARKET_CAP,
    MIN_LIQUIDITY,
    MIN_VOLUME_SPIKE,
    MAX_RUGCHECK_SCORE
)


class ReversalScanner:
    def __init__(self):
        self.dexscreener = DexScreenerClient()
        self.rugcheck = RugCheckClient()
        self.checked_tokens = set()

    def check_age(self, token_address: str) -> tuple[bool, int]:
        is_valid, created_at = self.dexscreener.check_token_age(token_address)
        
        if not is_valid or not created_at:
            return False, 0
        
        try:
            created_date = datetime.fromtimestamp(created_at / 1000)
            age = datetime.now() - created_date
            age_days = age.days
            return age_days >= MIN_AGE_DAYS, age_days
        except Exception as e:
            print(f"Error parsing age for {token_address}: {e}")
            return False, 0

    def check_market_cap(self, mc: float) -> bool:
        return MIN_MARKET_CAP <= mc <= MAX_MARKET_CAP

    def check_liquidity(self, liquidity: float) -> bool:
        return liquidity >= MIN_LIQUIDITY

    def check_volume_spike(self, volume_5m: float, buys_5m: int) -> tuple[bool, float, int]:
        has_spike = volume_5m >= MIN_VOLUME_SPIKE
        return has_spike, volume_5m, buys_5m

    def scan(self) -> List[dict]:
        results = []
        tokens = self.dexscreener.get_volume_spike_tokens(
            min_volume=MIN_VOLUME_SPIKE, 
            limit=50
        )
        
        print(f"[SCANNER] Found {len(tokens)} potential tokens to analyze...")
        
        for token in tokens:
            address = token.get("address", "")
            if address in self.checked_tokens:
                continue
            
            self.checked_tokens.add(address)
            symbol = token.get("symbol", "?")
            name = token.get("name", "Unknown")
            mc = token.get("market_cap", 0)
            liquidity = token.get("liquidity", 0)
            volume_5m = token.get("volume_5m", 0)
            buys_5m = token.get("buys_5m", 0)
            price_change = token.get("price_change_m5", 0)
            
            print(f"[SCANNER] Analyzing {symbol} ({address[:8]}...) | MC: ${mc:,.0f} | Vol5m: ${volume_5m:,.0f}")
            
            if not self.check_market_cap(mc):
                print(f"  ❌ Failed market cap filter (${mc:,.0f} not in range)")
                continue
            
            if not self.check_liquidity(liquidity):
                print(f"  ❌ Failed liquidity filter (${liquidity:,.0f} < ${MIN_LIQUIDITY:,})")
                continue
            
            is_old_enough, age_days = self.check_age(address)
            if not is_old_enough:
                print(f"  ❌ Failed age filter (only {age_days} days, need {MIN_AGE_DAYS}+)")
                continue
            
            is_safe, rug_result = self.rugcheck.is_safe(address, MAX_RUGCHECK_SCORE)
            if not is_safe:
                score = rug_result.get("score", 9999) if rug_result else 9999
                print(f"  ❌ Failed RugCheck (score: {score})")
                continue
            
            has_spike, vol_spike, buys = self.check_volume_spike(volume_5m, buys_5m)
            if not has_spike:
                print(f"  ❌ Failed volume spike filter (${vol_spike:,.0f} < ${MIN_VOLUME_SPIKE:,})")
                continue
            
            price_drop_pct = abs(price_change) if price_change < 0 else 50
            
            result = {
                "address": address,
                "symbol": symbol,
                "name": name,
                "age_days": age_days,
                "market_cap": mc,
                "liquidity": liquidity,
                "volume_5m": vol_spike,
                "buys_5m": buys,
                "price_drop_pct": price_drop_pct,
                "rug_score": rug_result.get("score", 0) if rug_result else 0,
                "rug_result": rug_result
            }
            
            results.append(result)
            print(f"  ✅ REVERSAL GEM FOUND: {symbol}! Age: {age_days}d, MC: ${mc:,.0f}, Vol5m: ${vol_spike:,.0f}")
        
        if len(self.checked_tokens) > 5000:
            self.checked_tokens = set()
        
        return results

    def close(self):
        self.dexscreener.close()


def create_scanner() -> ReversalScanner:
    return ReversalScanner()
