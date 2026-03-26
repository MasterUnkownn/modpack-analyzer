# =========================
# RECIPE ENGINE (REAL)
# =========================

import asyncio
from .registry import RecipeRegistry
from .analyzer import RecipeAnalyzer

class RecipeEngine:

    def __init__(self, bus):
        self.bus = bus
        self.registry = RecipeRegistry()
        self.analyzer = RecipeAnalyzer()

        self.bus.subscribe("datapack_recipes", self.on_datapack)

    async def on_datapack(self, recipes):
        self.registry.set(recipes)

    async def start(self):
        while True:
            grouped = self.registry.group_by_output()
            issues = self.analyzer.analyze(grouped)

            await self.bus.publish("recipe_issues", issues)

            await asyncio.sleep(10)
