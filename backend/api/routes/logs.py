# =========================
# LOG INGESTION API
# =========================

from fastapi import APIRouter, Request

router = APIRouter()

event_bus = None

@router.post("/logs")
async def ingest_logs(req: Request):
    body = await req.json()

    if event_bus:
        for line in body.get("lines", []):
            await event_bus.publish("log_line", {"raw": line})

    return {"status": "ok"}
