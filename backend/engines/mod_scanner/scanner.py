# =========================
# MOD SCANNER (REAL)
# =========================

import os
import asyncio
from .parser import ModParser

MODS_PATH = "./mods"

class ModScanner:

    def __init__(self, bus):
        self.bus = bus
        self.parser = ModParser()

    async def start(self):
        while True:
            mods = []

            if os.path.exists(MODS_PATH):
                for file in os.listdir(MODS_PATH):
                    if file.endswith(".jar"):
                        path = os.path.join(MODS_PATH, file)
                        mods.append(self.parser.parse_jar(path))

            await self.bus.publish("mods_updated", mods)

            await asyncio.sleep(15)
