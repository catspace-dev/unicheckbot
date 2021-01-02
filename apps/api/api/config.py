import os

# APP PORT
APP_PORT = os.environ.get("PORT", 8080)

# Node name. Will be shown in tgbot
NODE_NAME = os.environ.get("NODE_NAME", "Default node")

# Node location. Will be shown in tgbot
NODE_LOCATION = os.environ.get("NODE_LOCATION", "Undefined Location")

# Access token. Will be used for requests
ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN", "CHANGE_TOKEN_BY_ENV")
