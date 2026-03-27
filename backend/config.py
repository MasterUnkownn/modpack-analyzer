# =========================
# GLOBAL CONFIG
# =========================

import os

def get(key, default=None):
    return os.environ.get(key, default)


CONFIG = {
    "BACKEND_URL": get("BACKEND_URL", "http://localhost:8000"),
    "WS_URL": get("WS_URL", "ws://localhost:8000/ws"),
    "MODS_PATH": get("MODS_PATH", "./mods"),
    "LOG_PATH": get("LOG_PATH", "./logs/latest.log")
}
