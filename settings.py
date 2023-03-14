import os

TG_BOT_TOKEN = os.getenv("TG_BOT_TOKEN", "")
TG_ERRORS_CHAT_ID = os.getenv("TG_ERRORS_CHAT_ID", "")
TG_CHAT_ID = os.getenv("TG_CHAT_ID", "")
BINANCE_API_KEY = os.getenv("BINANCE_API_KEY", "")
BINANCE_SECRET_KEY = os.getenv("BINANCE_SECRET_KEY", "")

ALERT_TIME_THRESHOLD_IN_MINUTES = 10

CONFIGS = [
    {
        "label": "BINANCE_YM",
        "api_key": BINANCE_API_KEY,
        "secret_key": BINANCE_SECRET_KEY,
        "section": "USDT-M",
        "threshold": 26
    },
]
