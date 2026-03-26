# =========================
# ASSET PARSER (REAL)
# =========================

import zipfile
import json

class AssetParser:

    def parse_jar(self, path):
        assets = {
            "textures": set(),
            "models": [],
            "lang": set(),
            "tags": []
        }

        try:
            with zipfile.ZipFile(path) as jar:
                for file in jar.namelist():

                    # TEXTURES
                    if "/textures/" in file and file.endswith(".png"):
                        assets["textures"].add(file)

                    # MODELS
                    elif "/models/" in file and file.endswith(".json"):
                        try:
                            data = json.loads(jar.read(file).decode())
                            assets["models"].append({
                                "path": file,
                                "data": data
                            })
                        except:
                            pass

                    # LANG
                    elif "/lang/" in file and file.endswith(".json"):
                        try:
                            data = json.loads(jar.read(file).decode())
                            for key in data.keys():
                                assets["lang"].add(key)
                        except:
                            pass

                    # TAGS
                    elif "/tags/" in file and file.endswith(".json"):
                        try:
                            data = json.loads(jar.read(file).decode())
                            assets["tags"].append({
                                "path": file,
                                "data": data
                            })
                        except:
                            pass

        except Exception as e:
            print("Asset parse error:", e)

        return assets
