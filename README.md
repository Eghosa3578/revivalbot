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
   ```

3. **Install & Run:**
   ```bash
   pip install -r requirements.txt
   python main.py
   ```

## Filters

| Filter | Value |
|--------|-------|
| Min Age | 7 days |
| Market Cap | $10k - $200k |
| Liquidity | >= $10k |
| Volume Spike | > $5k (5min) |
| RugCheck Score | < 500 |

## API Sources

- **Scanner**: DexScreener API (free, no key required)
- **Safety Check**: RugCheck API (free, no key required)
- **Alerts**: Telegram Bot API

## Deploy to Railway

1. Push to GitHub
2. Connect repo to Railway
3. Set environment variables
4. Deploy
