# =========================
# CLUSTERING ENGINE (REAL)
# =========================

import asyncio
from collections import defaultdict

class ClusteringEngine:

    def __init__(self, bus):
        self.bus = bus
        self.errors = []

        self.bus.subscribe("errors_with_confidence", self.on_errors)

    async def on_errors(self, errors):
        self.errors = errors

    async def start(self):
        while True:
            clusters = defaultdict(list)

            for e in self.errors:
                key = f"{e['type']}::{e.get('source','unknown')}"
                clusters[key].append(e)

            result = []

            for k, items in clusters.items():
                result.append({
                    "type": items[0]["type"],
                    "source": items[0].get("source"),
                    "count": len(items),
                    "confidence": max(i["confidence"] for i in items)
                })

            await self.bus.publish("error_clusters", result)

            await asyncio.sleep(4)
