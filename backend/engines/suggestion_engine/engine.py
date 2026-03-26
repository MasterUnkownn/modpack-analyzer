# =========================
# SUGGESTION ENGINE (REAL)
# =========================

import asyncio

class SuggestionEngine:

    def __init__(self, bus, ws):
        self.bus = bus
        self.ws = ws
        self.clusters = []

        self.bus.subscribe("error_clusters", self.on_clusters)

    async def on_clusters(self, clusters):
        self.clusters = clusters

    async def start(self):
        while True:
            suggestions = []

            for c in self.clusters:

                t = c["type"]
                src = c.get("source")

                if t == "mod_error":
                    suggestions.append({
                        "title": f"Fix mod: {src}",
                        "action": "Update or remove mod"
                    })

                elif t == "missing_mod_server":
                    suggestions.append({
                        "title": f"Missing mod on server: {src}",
                        "action": "Install mod on server"
                    })

                elif t == "version_mismatch":
                    suggestions.append({
                        "title": f"Version mismatch: {src}",
                        "action": "Align mod versions"
                    })

                elif t == "recipe_issue":
                    suggestions.append({
                        "title": "Recipe conflict",
                        "action": "Remove duplicate via KubeJS"
                    })

                elif t == "asset_issue":
                    suggestions.append({
                        "title": "Missing asset",
                        "action": "Fix textures/models"
                    })

            if self.ws:
                await self.ws.broadcast({
                    "type": "suggestions",
                    "data": suggestions
                })

            await asyncio.sleep(5)
