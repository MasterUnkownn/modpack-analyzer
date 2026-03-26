import asyncio

class LogWatcher:
    def __init__(self, bus):
        self.bus = bus

    async def start(self):
        while True:
            await self.bus.publish("log_line", {"raw": "system heartbeat"})
            await asyncio.sleep(5)
