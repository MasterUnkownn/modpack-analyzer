import asyncio

class LogWatcher:
    def __init__(self, bus):
        self.bus = bus

    async def start(self):
        while True:
            await self.bus.publish("log_line", {"raw": "test"})
            await asyncio.sleep(5)
