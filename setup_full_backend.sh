#!/bin/bash

echo "🚀 Creating full backend..."

mkdir -p backend/{core,api/websocket,engines/{mod_scanner,log_watcher,datapack_engine,recipe_engine,asset_engine,comparison_engine,error_mapping_engine,confidence_engine,clustering_engine,suggestion_engine}}

# =========================
# MAIN
# =========================
cat > backend/main.py << 'EOF'
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
EOF

# =========================
# REQUIREMENTS
# =========================
cat > backend/requirements.txt << 'EOF'
fastapi==0.95.2
uvicorn
requests
EOF

# =========================
# CORE
# =========================
cat > backend/core/event_bus.py << 'EOF'
class EventBus:
    def __init__(self):
        self.listeners = {}

    def subscribe(self, event, callback):
        self.listeners.setdefault(event, []).append(callback)

    async def publish(self, event, data):
        for cb in self.listeners.get(event, []):
            await cb(data)
EOF

cat > backend/core/engine_manager.py << 'EOF'
import asyncio

class EngineManager:
    def __init__(self, engines):
        self.engines = engines

    async def start_all(self):
        for e in self.engines:
            asyncio.create_task(e.start())
EOF

# =========================
# WEBSOCKET
# =========================
cat > backend/api/websocket/manager.py << 'EOF'
class WebSocketManager:
    def __init__(self):
        self.clients = []

    async def connect(self, ws):
        await ws.accept()
        self.clients.append(ws)

    def disconnect(self, ws):
        if ws in self.clients:
            self.clients.remove(ws)

    async def broadcast(self, data):
        for c in self.clients:
            try:
                await c.send_json(data)
            except:
                pass
EOF

# =========================
# BASIC ENGINES TEMPLATE
# =========================
create_engine () {
cat > $1 << EOF
import asyncio

class $(basename $(dirname $1) | sed 's/.*/\u&/' | sed 's/_//g'):
    def __init__(self, bus):
        self.bus = bus

    async def start(self):
        while True:
            await asyncio.sleep(5)
EOF
}

# Mod scanner
cat > backend/engines/mod_scanner/scanner.py << 'EOF'
import os, asyncio

class ModScanner:
    def __init__(self, bus):
        self.bus = bus

    async def start(self):
        while True:
            mods = []
            if os.path.exists("mods"):
                for f in os.listdir("mods"):
                    if f.endswith(".jar"):
                        mods.append({"name": f, "mod_id": f.lower()})
            await self.bus.publish("mods_updated", mods)
            await asyncio.sleep(10)
EOF

# Log watcher
cat > backend/engines/log_watcher/watcher.py << 'EOF'
import asyncio

class LogWatcher:
    def __init__(self, bus):
        self.bus = bus

    async def start(self):
        while True:
            await self.bus.publish("log_line", {"raw": "test"})
            await asyncio.sleep(5)
EOF

# Simple engines
for engine in datapack_engine recipe_engine asset_engine comparison_engine error_mapping_engine confidence_engine clustering_engine suggestion_engine
do
mkdir -p backend/engines/$engine
cat > backend/engines/$engine/engine.py << EOF
import asyncio

class ${engine^}:
    def __init__(self, bus, ws=None):
        self.bus = bus
        self.ws = ws

    async def start(self):
        while True:
            await asyncio.sleep(5)
EOF
done

echo "✅ Backend fully created!"
