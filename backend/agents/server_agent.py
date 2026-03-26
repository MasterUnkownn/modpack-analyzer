# =========================
# SERVER AGENT (LOG STREAM)
# =========================

import time
import requests
import os

LOG_PATH = "./logs/latest.log"
BACKEND = "http://YOUR_PHONE_IP:8000/api/logs"

def follow(file):
    file.seek(0, 2)
    while True:
        line = file.readline()
        if not line:
            time.sleep(0.2)
            continue
        yield line.strip()

def run():
    if not os.path.exists(LOG_PATH):
        print("Log file not found")
        return

    with open(LOG_PATH, "r", encoding="utf-8", errors="ignore") as f:
        for line in follow(f):
            try:
                requests.post(BACKEND, json={"lines": [line]})
                print("Sent:", line[:80])
            except Exception as e:
                print("Error:", e)

if __name__ == "__main__":
    run()
