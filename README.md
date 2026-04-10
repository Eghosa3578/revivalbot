# Reversal Sniper Bot

Scans Solana blockchain for "dead" memecoins showing signs of life (volume spikes).

## Setup

1. **Get Telegram Bot Token:**
   - Message @BotFather on Telegram
   - Create new bot and copy the token

2. **Configure Environment:**
   ```
   cp .env.example .env
   ```
   Edit `.env`:
   ```
TELEGRAM_BOT_TOKEN=your_telegram_token
TELEGRAM_CHAT_ID=your_chat_id
# Operational mode for filters
FILTER_MODE=Balanced
   ```

3. **Install & Run:**
   ```bash
   pip install -r requirements.txt
   python main.py
   ```

## Filters

| Filter | Balanced (Mode: Balanced) |
|--------|---------------------------|
| Min Age | 3 days |
| Market Cap | $5k - $500k |
| Liquidity | >= $5k |
| Volume Spike | > $2k (15m) |
| RugCheck Score | < 800 |

Notes: You can switch modes with FILTER_MODE in the environment. Current default is Balanced.

## API Sources

- **Scanner**: DexScreener API (free, no key required)
- **Safety Check**: RugCheck API (free, no key required)
- **Alerts**: Telegram Bot API

## Deploy to Railway

1. Push to GitHub
2. Connect repo to Railway
3. Set environment variables
4. Deploy
