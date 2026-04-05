import os
from dotenv import load_dotenv

load_dotenv()

BIRDEYE_API_KEY = os.getenv("BIRDEYE_API_KEY", "")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "revivalmemebot")

MIN_AGE_DAYS = 7
MIN_MARKET_CAP = 10_000
MAX_MARKET_CAP = 200_000
MIN_LIQUIDITY = 10_000
MIN_VOLUME_SPIKE = 5_000
MAX_RUGCHECK_SCORE = 500
SCAN_INTERVAL = 60

DEXSCREENER_BASE_URL = "https://api.dexscreener.com"
