import os

# Loading token from .env
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Influx for metrics
INFLUX_HOST = os.getenv("INFLUX_HOST", None)
INFLUX_PORT = os.getenv("INFLUX_PORT", None)
INFLUX_USERNAME = os.getenv("INFLUX_USERNAME", None)
INFLUX_PASSWORD = os.getenv("INFLUX_PASSWORD", None)
INFLUX_DB = os.getenv("INFLUX_DB", None)

# Notifications
NOTIFICATION_BOT_TOKEN = os.getenv("NOTIFICATION_BOT_TOKEN")
NOTIFICATION_USERS = os.getenv("NOTIFICATION_USERS", "").split(",")
