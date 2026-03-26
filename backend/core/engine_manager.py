import asyncio

class EngineManager:
    def __init__(self, engines):
        self.engines = engines

    async def start_all(self):
        for e in self.engines:
            asyncio.create_task(e.start())
