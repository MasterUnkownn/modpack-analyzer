# =========================
# INSTANCE API
# =========================

from fastapi import APIRouter, Request

router = APIRouter()

instance_manager = None

@router.post("/instance/update")
async def update_instance(req: Request):
    body = await req.json()

    if instance_manager:
        await instance_manager.update_instance(
            body["instance_id"],
            body["instance_type"],
            body["mods"]
        )

    return {"status": "ok"}
