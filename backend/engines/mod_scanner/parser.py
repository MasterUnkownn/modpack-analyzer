# =========================
# MOD PARSER (REAL)
# =========================

import zipfile

class ModParser:

    def parse_jar(self, path):
        data = {
            "name": path.split("/")[-1],
            "mod_id": None,
            "version": None
        }

        try:
            with zipfile.ZipFile(path) as jar:

                # Forge / NeoForge
                if "META-INF/mods.toml" in jar.namelist():
                    content = jar.read("META-INF/mods.toml").decode()

                    for line in content.splitlines():
                        if "modId" in line:
                            data["mod_id"] = line.split("=")[-1].replace('"','').strip()
                        if "version" in line:
                            data["version"] = line.split("=")[-1].replace('"','').strip()

                # Fallback
                if not data["mod_id"]:
                    data["mod_id"] = data["name"].lower()

        except Exception as e:
            print("Mod parse error:", e)

        return data
