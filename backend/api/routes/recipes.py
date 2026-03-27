# =========================
# RECIPE SAVE API (UNIVERSAL)
# =========================

from fastapi import APIRouter, Request
from core.datapack_builder import DatapackBuilder
from core.recipe_converter import convert_recipe

router = APIRouter()
builder = DatapackBuilder()

@router.post("/recipes/save")
async def save_recipe(req: Request):
    body = await req.json()

    recipe_json = convert_recipe(body)

    original_path = body.get("original_path", "custom/generated")

    if ":" in original_path:
        namespace, path = original_path.split(":", 1)
    else:
        namespace = "custom"
        path = original_path

    saved_path = builder.save_recipe(namespace, path, recipe_json)

    return {
        "status": "saved",
        "path": saved_path,
        "type": recipe_json.get("type")
    }
