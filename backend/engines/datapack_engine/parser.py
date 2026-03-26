# =========================
# DATAPACK PARSER (REAL)
# =========================

import os
import json
import zipfile

class DatapackParser:

    def parse_folder(self, path):
        recipes = []

        for root, _, files in os.walk(path):
            for file in files:
                if file.endswith(".json") and "recipes" in root:
                    full = os.path.join(root, file)

                    try:
                        with open(full) as f:
                            data = json.load(f)

                            recipes.append({
                                "source": "datapack",
                                "path": full,
                                "type": data.get("type"),
                                "output": data.get("result"),
                                "raw": data
                            })
                    except:
                        pass

        return recipes

    def parse_zip(self, path):
        recipes = []

        with zipfile.ZipFile(path) as z:
            for file in z.namelist():
                if file.endswith(".json") and "recipes" in file:
                    try:
                        data = json.loads(z.read(file).decode())

                        recipes.append({
                            "source": "datapack",
                            "path": file,
                            "type": data.get("type"),
                            "output": data.get("result"),
                            "raw": data
                        })
                    except:
                        pass

        return recipes
