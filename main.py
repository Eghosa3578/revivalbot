import time
import signal
import sys
from datetime import datetime
from scanner import create_scanner
from telegram_bot import get_telegram_bot
from config import SCAN_INTERVAL


class ReversalBot:
    def __init__(self):
        self.scanner = create_scanner()
        self.telegram = get_telegram_bot()
        self.running = True
        self.scan_count = 0
        
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

    def _signal_handler(self, signum, frame):
        print("\n[SHUTDOWN] Received shutdown signal, stopping...")
        self.running = False

    def run(self):
        print("=" * 60)
        print("🔍 REVERSAL SNIPER BOT - Starting...")
        print(f"⏱️  Scan interval: {SCAN_INTERVAL} seconds")
        print("📋 Filters: Age≥7d, MC $10k-$200k, Liq≥$10k, Vol spike≥$5k")
        print("=" * 60)
        
        while self.running:
            try:
                self.scan_count += 1
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f"\n[SCAN #{self.scan_count}] {timestamp}")
                
                gems = self.scanner.scan()
                
                for gem in gems:
                    print(f"  📤 Sending Telegram alert for {gem['symbol']}...")
                    self.telegram.send_reversal_alert(gem)
                    print(f"  ✅ Alert sent!")
                
                if not gems:
                    print(f"[SCAN #{self.scan_count}] No reversal gems found in this cycle.")
                
                print(f"[STATUS] Next scan in {SCAN_INTERVAL} seconds...")
                time.sleep(SCAN_INTERVAL)
                
            except Exception as e:
                print(f"[ERROR] Scan cycle failed: {e}")
                time.sleep(10)
        
        self.cleanup()

    def cleanup(self):
        print("[CLEANUP] Closing connections...")
        self.scanner.close()
        print("[DONE] Bot shutdown complete.")


def main():
    print("\n" + "=" * 60)
    print("🔴 REVERSAL SNIPER BOT v1.0")
    print("=" * 60)
    
    try:
        bot = ReversalBot()
        bot.run()
    except KeyboardInterrupt:
        print("\n[SHUTDOWN] Interrupted by user.")
        sys.exit(0)


if __name__ == "__main__":
    main()
