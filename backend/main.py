# =========================
# MAIN ENTRYPOINT (FULL)
# =========================

from fastapi import FastAPI, WebSocket
import asyncio

# CORE
from core.event_bus import EventBus
from core.engine_manager import EngineManager

# WEBSOCKET
from api.websocket.manager import WebSocketManager

# ROUTES
from api.routes import instance, logs, recipes

# ENGINES
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
from engines.instance_manager.engine import InstanceManagerEngine

# =========================
# INIT
# =========================

app = FastAPI()

event_bus = EventBus()
ws_manager = WebSocketManager()

# =========================
# ENGINES
# =========================

instance_engine = InstanceManagerEngine(event_bus)

engine_manager = EngineManager([
    instance_engine,

    ModScanner(event_bus),
    LogWatcher(event_bus),
    DatapackEngine(event_bus),
    RecipeEngine(event_bus),
    AssetEngine(event_bus),

    ComparisonEngine(event_bus, ws_manager),
    ErrorMappingEngine(event_bus, ws_manager),
    ConfidenceEngine(event_bus),
    ClusteringEngine(event_bus),
    SuggestionEngine(event_bus, ws_manager),
])

# =========================
# STARTUP
# =========================

@app.on_event("startup")
async def startup():
    print("🚀 Starting engines...")
    asyncio.create_task(engine_manager.start_all())

# =========================
# WEBSOCKET
# =========================

@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws_manager.connect(ws)

    try:
        while True:
            await ws.receive_text()
    except:
        ws_manager.disconnect(ws)

# =========================
# ROUTES
# =========================

app.include_router(instance.router, prefix="/api")
app.include_router(logs.router, prefix="/api")
logs.event_bus = event_bus
app.include_router(recipes.router, prefix="/api")
# Inject instance manager into route
instance.instance_manager = instance_engine

# =========================
# HEALTH CHECK
# =========================

@app.get("/")
def root():
    return {
        "status": "running",
        "engines": len(engine_manager.engines)
    }
