from fastapi import FastAPI, WebSocket
import asyncio

from core.event_bus import EventBus
from core.engine_manager import EngineManager
from api.websocket.manager import WebSocketManager

from engines.mod_scanner.scanner import ModScanner
from engines.log_watcher.watcher import LogWatcher
from engines.datapack_engine.engine import DatapackEngine
from engines.recipe_engine.engine import RecipeEngine
from engines.asset_engine.engine import AssetEngine
from engines.comparison_engine.engine import ComparisonEngine
from engines.error_mapping_engine.engine import ErrorMappingEngine
from engines.confidence_engine.engine import ConfidenceEngine
from engines.clustering_engine.engine import ClusteringEngine
from engines.suggestion_engine.engine import SuggestionEngine

app = FastAPI()

bus = EventBus()
ws = WebSocketManager()

engine_manager = EngineManager([
    ModScanner(bus),
    LogWatcher(bus),
    DatapackEngine(bus),
    RecipeEngine(bus),
    AssetEngine(bus),
    ComparisonEngine(bus, ws),
    ErrorMappingEngine(bus, ws),
    ConfidenceEngine(bus),
    ClusteringEngine(bus),
    SuggestionEngine(bus, ws),
])

@app.on_event("startup")
async def startup():
    asyncio.create_task(engine_manager.start_all())

@app.websocket("/ws")
async def websocket(wsock: WebSocket):
    await ws.connect(wsock)
    try:
        while True:
            await wsock.receive_text()
    except:
        ws.disconnect(wsock)

@app.get("/")
def root():
    return {"status": "running"}
