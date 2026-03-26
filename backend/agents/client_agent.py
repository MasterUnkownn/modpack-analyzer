# =========================
# CLIENT AGENT
# =========================

import os
import time
import requests

BACKEND = "http://YOUR_PHONE_IP:8000/api/instance/update"
MODS_PATH = "./mods"

def scan_mods():
    mods = []

    if os.path.exists(MODS_PATH):
        for f in os.listdir(MODS_PATH):
            if f.endswith(".jar"):
                mods.append({
                    "name": f,
                    "mod_id": f.lower()
                })

    return mods


def loop():
    while True:
        data = {
            "instance_id": "client",
            "instance_type": "client",
            "mods": scan_mods()
        }

        try:
            requests.post(BACKEND, json=data)
            print("Synced")
        except Exception as e:
            print("Sync failed:", e)

        time.sleep(10)


if __name__ == "__main__":
    loop()
