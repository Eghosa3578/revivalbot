import os
from dotenv import load_dotenv

load_dotenv()

# Telegram credentials (unchanged)
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

# Operational mode for filters
FILTER_MODE = os.getenv("FILTER_MODE", "Balanced").strip()

# Thresholds by mode (values are in USD where applicable)
THRESHOLDS = {
    "Conservative": {
        "MIN_AGE_DAYS": 7,
        "MIN_MARKET_CAP": 10000,
        "MAX_MARKET_CAP": 200000,
        "MIN_LIQUIDITY": 10000,
        "MIN_VOLUME_SPIKE": 5000,
        "MAX_RUGCHECK_SCORE": 500,
    },
    "Balanced": {
        "MIN_AGE_DAYS": 3,
        "MIN_MARKET_CAP": 5000,
        "MAX_MARKET_CAP": 500000,
        "MIN_LIQUIDITY": 5000,
        "MIN_VOLUME_SPIKE": 2000,
        "MAX_RUGCHECK_SCORE": 800,
    },
    "Aggressive": {
        "MIN_AGE_DAYS": 1,
        "MIN_MARKET_CAP": 1000,
        "MAX_MARKET_CAP": 2000000,
        "MIN_LIQUIDITY": 2000,
        "MIN_VOLUME_SPIKE": 1000,
        "MAX_RUGCHECK_SCORE": 1000,
    },
}

# Resolve thresholds for the active mode, defaulting to Balanced if unknown
TH = THRESHOLDS.get(FILTER_MODE, THRESHOLDS["Balanced"])

MIN_AGE_DAYS = TH["MIN_AGE_DAYS"]
MIN_MARKET_CAP = TH["MIN_MARKET_CAP"]
MAX_MARKET_CAP = TH["MAX_MARKET_CAP"]
MIN_LIQUIDITY = TH["MIN_LIQUIDITY"]
MIN_VOLUME_SPIKE = TH["MIN_VOLUME_SPIKE"]
MAX_RUGCHECK_SCORE = TH["MAX_RUGCHECK_SCORE"]

DEXSCREENER_BASE_URL = "https://api.dexscreener.com"
ENABLE_TOKEN_BOOSTS = os.getenv("ENABLE_TOKEN_BOOSTS", "false").lower() in ("true","1","yes","y")
BOOST_COOLDOWN_SEC = int(os.getenv("BOOST_COOLDOWN_SEC", "300"))
SCAN_INTERVAL = int(os.getenv("SCAN_INTERVAL", "60"))
