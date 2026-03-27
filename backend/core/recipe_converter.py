# =========================
# UNIVERSAL RECIPE CONVERTER
# =========================

def grid_to_shaped(grid, output):

    pattern = []
    key = {}
    char_code = ord("A")
    item_map = {}

    for row in grid["slots"]:
        line = ""
        for cell in row:
            if cell:
                if cell not in item_map:
                    char = chr(char_code)
                    item_map[cell] = char
                    key[char] = {"item": cell}
                    char_code += 1
                line += item_map[cell]
            else:
                line += " "
        pattern.append(line)

    return {
        "type": "minecraft:crafting_shaped",
        "pattern": pattern,
        "key": key,
        "result": {
            "item": output
        }
    }


def grid_to_shapeless(grid, output):

    ingredients = []

    for row in grid["slots"]:
        for cell in row:
            if cell:
                ingredients.append({"item": cell})

    return {
        "type": "minecraft:crafting_shapeless",
        "ingredients": ingredients,
        "result": {
            "item": output
        }
    }


def convert_recipe(data):

    rtype = data.get("type", "shaped")
    grid = data.get("grid")
    output = data.get("output")

    # =========================
    # SHAPED
    # =========================
    if rtype == "shaped":
        return grid_to_shaped(grid, output)

    # =========================
    # SHAPELESS
    # =========================
    if rtype == "shapeless":
        return grid_to_shapeless(grid, output)

    # =========================
    # CUSTOM / MODDED
    # =========================
    if rtype == "custom":
        return data.get("raw", {})

    # fallback
    return grid_to_shaped(grid, output)
