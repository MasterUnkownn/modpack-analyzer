# =========================
# ASSET ENGINE (REAL)
# =========================

import os
import asyncio
from .parser import AssetParser
from .analyzer import AssetAnalyzer

MODS_PATH = "./mods"

class AssetEngine:

    def __init__(self, bus):
        self.bus = bus
        self.parser = AssetParser()
        self.analyzer = AssetAnalyzer()

    async def start(self):
        while True:
            combined = {
                "textures": set(),
                "models": [],
                "lang": set(),
                "tags": []
            }

            if os.path.exists(MODS_PATH):
                for file in os.listdir(MODS_PATH):
                    if file.endswith(".jar"):
                        path = os.path.join(MODS_PATH, file)

                        data = self.parser.parse_jar(path)

                        combined["textures"].update(data["textures"])
                        combined["models"].extend(data["models"])
                        combined["lang"].update(data["lang"])
                        combined["tags"].extend(data["tags"])

            issues = self.analyzer.analyze(combined)

            await self.bus.publish("asset_issues", issues)

            await asyncio.sleep(25)
