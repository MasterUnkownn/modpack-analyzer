# =========================
# ERROR MAPPING ENGINE (REAL)
# =========================

import asyncio
import re

class ErrorMappingEngine:

    def __init__(self, bus, ws):
        self.bus = bus
        self.ws = ws

        self.logs = []
        self.mods = []
        self.recipe_issues = []
        self.asset_issues = []
        self.comparison = {}

        self.bus.subscribe("log_line", self.on_log)
        self.bus.subscribe("mods_updated", self.on_mods)
        self.bus.subscribe("recipe_issues", self.on_recipe)
        self.bus.subscribe("asset_issues", self.on_asset)
        self.bus.subscribe("comparison", self.on_comparison)

    async def on_log(self, log):
        self.logs.append(log)
        self.logs = self.logs[-200:]

    async def on_mods(self, mods):
        self.mods = mods

    async def on_recipe(self, issues):
        self.recipe_issues = issues

    async def on_asset(self, issues):
        self.asset_issues = issues

    async def on_comparison(self, data):
        self.comparison = data

    async def start(self):
        while True:
            mapped = []

            # LOG → MOD
            for log in self.logs:
                line = log.get("raw", "")

                match = re.search(r'at ([\w\.]+)', line)
                if match:
                    pkg = match.group(1)

                    for mod in self.mods:
                        if mod["mod_id"] and mod["mod_id"] in pkg:
                            mapped.append({
                                "type": "mod_error",
                                "source": mod["mod_id"],
                                "message": line
                            })

                if "kubejs" in line.lower():
                    mapped.append({
                        "type": "kubejs_error",
                        "source": "kubejs",
                        "message": line
                    })

            # RECIPE
            for r in self.recipe_issues:
                mapped.append({
                    "type": "recipe_issue",
                    "message": r["message"]
                })

            # ASSET
            for a in self.asset_issues:
                mapped.append({
                    "type": "asset_issue",
                    "message": a["message"]
                })

            # COMPARISON
            for mod in self.comparison.get("missing_on_server", []):
                mapped.append({
                    "type": "missing_mod_server",
                    "source": mod
                })

            for mod in self.comparison.get("version_mismatch", []):
                mapped.append({
                    "type": "version_mismatch",
                    "source": mod
                })

            await self.bus.publish("mapped_errors", mapped)

            if self.ws:
                await self.ws.broadcast({
                    "type": "mapped_errors",
                    "data": mapped
                })

            await asyncio.sleep(5)
