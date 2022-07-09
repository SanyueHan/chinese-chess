import os


DEVELOPER_MODE = bool(os.environ.get("DEV_MODE"))
AI_SEARCH_DEPTH = int(os.environ.get("AI_SEARCH_DEPTH", 4))
