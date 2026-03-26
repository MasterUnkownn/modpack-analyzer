# =========================
# RECIPE ANALYZER
# =========================

class RecipeAnalyzer:

    def analyze(self, grouped):
        issues = []

        for output, recipes in grouped.items():

            if len(recipes) > 1:
                issues.append({
                    "type": "recipe_conflict",
                    "message": f"{len(recipes)} recipes produce {output}"
                })

            if output == "None":
                issues.append({
                    "type": "invalid_recipe",
                    "message": "Recipe missing output"
                })

        return issues
