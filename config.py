import os


DEVELOPER_MODE = bool(os.environ.get("DEV_MODE"))
AI_SEARCH_DEPTH = int(os.environ.get("AI_SEARCH_DEPTH", 4))


print(f"DEVELOPER_MODE: {DEVELOPER_MODE}")
print(f"AI_SEARCH_DEPTH: {AI_SEARCH_DEPTH}")
