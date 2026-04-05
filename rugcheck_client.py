import rugcheck as rugcheck_lib
from typing import Optional


class RugCheckClient:
    def check_token(self, token_address: str) -> Optional[dict]:
        try:
            result = rugcheck_lib.rugcheck(token_address)
            return {
                "score": getattr(result, "score", 9999),
                "rugged": getattr(result, "rugged", True),
                "risks": getattr(result, "risks", []),
                "mint_authority": getattr(result, "mintAuthority", None),
                "freeze_authority": getattr(result, "freezeAuthority", None),
                "total_market_liquidity": getattr(result, "totalMarketLiquidity", 0),
                "top_holders": getattr(result, "topHolders", []),
                "summary": getattr(result, "summary", ""),
                "to_dict": result.to_dict()
            }
        except Exception as e:
            print(f"RugCheck error for {token_address}: {e}")
            return None

    def is_safe(self, token_address: str, max_score: int = 500) -> tuple[bool, Optional[dict]]:
        result = self.check_token(token_address)
        if not result:
            return False, None
        
        score = result["score"]
        is_safe = score < max_score and not result["rugged"]
        
        return is_safe, result

    def format_risks(self, risks: list) -> str:
        if not risks:
            return "No major risks detected"
        
        formatted = []
        for risk in risks[:5]:
            level = risk.get("level", "unknown")
            name = risk.get("name", "Unknown risk")
            score_val = risk.get("score", 0)
            formatted.append(f"• {name} ({level}, score: {score_val})")
        
        return "\n".join(formatted)


def get_rugcheck_client() -> RugCheckClient:
    return RugCheckClient()
