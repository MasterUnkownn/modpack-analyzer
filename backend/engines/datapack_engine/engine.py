# =========================
# DATAPACK ENGINE (REAL)
# =========================

import os
import asyncio
from .parser import DatapackParser

DATAPACK_PATH = "./world/datapacks"

class DatapackEngine:

    def __init__(self, bus):
        self.bus = bus
        self.parser = DatapackParser()

    async def start(self):
        while True:
            recipes = []

            if os.path.exists(DATAPACK_PATH):
                for entry in os.listdir(DATAPACK_PATH):
                    path = os.path.join(DATAPACK_PATH, entry)

                    if os.path.isdir(path):
                        recipes.extend(self.parser.parse_folder(path))
                    elif entry.endswith(".zip"):
                        recipes.extend(self.parser.parse_zip(path))

            await self.bus.publish("datapack_recipes", recipes)

            await asyncio.sleep(20)
