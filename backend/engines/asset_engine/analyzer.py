# =========================
# ASSET ANALYZER (REAL)
# =========================

class AssetAnalyzer:

    def analyze(self, assets):
        issues = []

        textures = assets["textures"]

        # Missing textures in models
        for model in assets["models"]:
            tex = model["data"].get("textures", {})

            for t in tex.values():
                if t not in textures:
                    issues.append({
                        "type": "missing_texture",
                        "message": f"Missing texture: {t}"
                    })

        # Empty tags
        for tag in assets["tags"]:
            if not tag["data"].get("values"):
                issues.append({
                    "type": "empty_tag",
                    "message": f"Empty tag: {tag['path']}"
                })

        return issues
