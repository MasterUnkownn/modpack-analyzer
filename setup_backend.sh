#!/bin/bash

echo "Creating backend structure..."

mkdir -p backend/{core,api/routes,api/websocket,engines,models,database}

# main.py
cat > backend/main.py << 'EOF'
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"status": "running"}
EOF

# requirements.txt
cat > backend/requirements.txt << 'EOF'
fastapi==0.95.2
uvicorn
requests
EOF

# event_bus
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

# websocket manager
mkdir -p backend/api/websocket
cat > backend/api/websocket/manager.py << 'EOF'
class WebSocketManager:
    def __init__(self):
        self.clients = []

    async def connect(self, ws):
        await ws.accept()
        self.clients.append(ws)

    def disconnect(self, ws):
        self.clients.remove(ws)

    async def broadcast(self, data):
        for c in self.clients:
            await c.send_json(data)
EOF

echo "Backend base created."
