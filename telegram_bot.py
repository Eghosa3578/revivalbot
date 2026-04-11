import asyncio
import telegram
from typing import Optional
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
from datetime import datetime
from urllib.parse import quote_plus
"""Note: keep imports minimal; we format messages using HTML for Telegram.
"""
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID


class TelegramBot:
    def __init__(self):
        self.bot_token = TELEGRAM_BOT_TOKEN
        self.chat_id = TELEGRAM_CHAT_ID
        self.client = telegram.Bot(token=self.bot_token)

    async def send_message(self, text: str) -> bool:
        try:
            await self.client.send_message(
                chat_id=self.chat_id,
                text=text,
                parse_mode="HTML"
            )
            return True
        except Exception as e:
            print(f"Telegram send error: {e}")
            return False

    def send_reversal_alert(self, token_data: dict) -> bool:
        symbol = token_data.get("symbol", "UNKNOWN")
        name = token_data.get("name", "Unknown Token")
        address = token_data.get("address", "")
        age_days = token_data.get("age_days", 0)
        market_cap = token_data.get("market_cap", 0)
        volume_1h = token_data.get("volume_1h", 0)
        volume_24h = token_data.get("volume_24h", 0)
        liquidity = token_data.get("liquidity", 0)
        price_drop_pct = token_data.get("price_drop_pct", 0)
        rug_score = token_data.get("rug_score", 0)
        rug_check_url = f"https://rugcheck.xyz/tokens/{address}"
        dex_url = f"https://dexscreener.com/solana/{address}"
        # Address is shown in code block for easy copying in UI
        message = f"""🚨 <b>NEW GEM DETECTED!</b> 🚨

🪙 <b>Token:</b> {name} ({symbol})
🔗 <b>CA:</b> <code>{address}</code>
⏳ <b>Age:</b> {age_days} Days Old
💰 <b>Market Cap:</b> ${market_cap:,.0f}

📊 <b>THE PULSE:</b>
🔊 Volume (1h): <b>${volume_1h:,.0f}</b> | <b>Vol 24h:</b> <b>${volume_24h:,.0f}</b>
💧 Liquidity: ${liquidity:,.0f}

🛡️ <b>Safety:</b>
🔎 RugCheck Score: <b>{rug_score}</b>

🔗 <a href="{dex_url}">DexScreener Chart</a> | <a href="{rug_check_url}">RugCheck Report</a>

<i>Reversal Bot - Scanning for dead coins with pulse...</i>"""

        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                asyncio.create_task(self.send_message(message))
            else:
                loop.run_until_complete(self.send_message(message))
            return True
        except Exception as e:
            print(f"Failed to send Telegram alert: {e}")
            return False


def get_telegram_bot() -> TelegramBot:
    return TelegramBot()
