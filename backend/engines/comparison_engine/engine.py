import asyncio

class ComparisonEngine:
    def __init__(self, bus, ws=None):
        self.bus = bus
        self.ws = ws

    async def start(self):
        while True:
            await asyncio.sleep(5)
