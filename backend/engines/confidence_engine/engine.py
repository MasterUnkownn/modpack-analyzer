# =========================
# CONFIDENCE ENGINE (REAL)
# =========================

import asyncio

class ConfidenceEngine:

    def __init__(self, bus):
        self.bus = bus
        self.errors = []

        self.bus.subscribe("mapped_errors", self.on_errors)

    async def on_errors(self, errors):
        self.errors = errors

    async def start(self):
        while True:
            enriched = []

            for e in self.errors:
                score = 0.5

                if e["type"] == "mod_error":
                    score = 0.9
                elif e["type"] == "missing_mod_server":
                    score = 0.95
                elif e["type"] == "asset_issue":
                    score = 0.8
                elif e["type"] == "recipe_issue":
                    score = 0.75

                e["confidence"] = score
                enriched.append(e)

            await self.bus.publish("errors_with_confidence", enriched)

            await asyncio.sleep(3)
