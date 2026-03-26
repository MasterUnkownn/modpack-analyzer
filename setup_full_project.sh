#!/bin/bash

echo "🚀 Creating FULL Modpack Analyzer Project..."

# =========================
# ROOT STRUCTURE
# =========================
mkdir -p backend/{core,api/websocket,engines/{mod_scanner,log_watcher,datapack_engine,recipe_engine,asset_engine,comparison_engine,error_mapping_engine,confidence_engine,clustering_engine,suggestion_engine}}
mkdir -p frontend/src/{pages,components,services,styles}
mkdir -p scripts

# =========================
# BACKEND MAIN
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
# ENGINE TEMPLATES
# =========================

create_engine () {
cat > $1 << EOF
import asyncio

class ${2}:
    def __init__(self, bus, ws=None):
        self.bus = bus
        self.ws = ws

    async def start(self):
        while True:
            await asyncio.sleep(5)
EOF
}

# Mod Scanner
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
            await self.bus.publish("log_line", {"raw": "test log"})
            await asyncio.sleep(5)
EOF

# Generic engines
create_engine backend/engines/datapack_engine/engine.py DatapackEngine
create_engine backend/engines/recipe_engine/engine.py RecipeEngine
create_engine backend/engines/asset_engine/engine.py AssetEngine
create_engine backend/engines/comparison_engine/engine.py ComparisonEngine
create_engine backend/engines/error_mapping_engine/engine.py ErrorMappingEngine
create_engine backend/engines/confidence_engine/engine.py ConfidenceEngine
create_engine backend/engines/clustering_engine/engine.py ClusteringEngine
create_engine backend/engines/suggestion_engine/engine.py SuggestionEngine

# =========================
# FRONTEND (MINIMAL)
# =========================
cat > frontend/index.html << 'EOF'
<!DOCTYPE html>
<html>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.jsx"></script>
  </body>
</html>
EOF

cat > frontend/src/main.jsx << 'EOF'
import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";

ReactDOM.createRoot(document.getElementById("root")).render(<App />);
EOF

cat > frontend/src/App.jsx << 'EOF'
export default function App(){
  return <h1>Modpack Analyzer Running 🚀</h1>
}
EOF

cat > frontend/package.json << 'EOF'
{
  "name": "modpack-analyzer",
  "version": "1.0.0",
  "scripts": {
    "dev": "vite"
  },
  "dependencies": {
    "react": "^18",
    "react-dom": "^18"
  }
}
EOF

# =========================
# ENV + GIT
# =========================
cat > .env.example << 'EOF'
CURSEFORGE_API_KEY=your_key_here
EOF

cat > .gitignore << 'EOF'
__pycache__/
*.pyc
.env
node_modules/
EOF

# =========================
# DEV SCRIPTS
# =========================
cat > scripts/dev.sh << 'EOF'
#!/bin/bash
cd backend
python -m uvicorn main:app --host 0.0.0.0 --port 8000 &
cd ../frontend
npm install
npm run dev
EOF

chmod +x scripts/dev.sh

echo "✅ FULL PROJECT CREATED SUCCESSFULLY!"
