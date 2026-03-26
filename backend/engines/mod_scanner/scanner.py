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
