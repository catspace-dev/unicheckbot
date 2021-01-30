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

# Mysql params
MYSQL_HOST = os.getenv("MYSQL_HOST", None)  # if none, use sqlite db
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_PORT = os.getenv("MYSQL_PORT", 3306)
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "unicheckbot")
