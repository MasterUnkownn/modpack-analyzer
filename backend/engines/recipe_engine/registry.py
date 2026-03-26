# =========================
# RECIPE REGISTRY
# =========================

class RecipeRegistry:

    def __init__(self):
        self.recipes = []

    def set(self, recipes):
        self.recipes = recipes

    def group_by_output(self):
        grouped = {}

        for r in self.recipes:
            out = str(r.get("output"))

            if out not in grouped:
                grouped[out] = []

            grouped[out].append(r)

        return grouped
