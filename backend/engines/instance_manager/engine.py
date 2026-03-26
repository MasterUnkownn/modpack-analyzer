# =========================
# INSTANCE MANAGER ENGINE
# =========================

import asyncio

class InstanceManagerEngine:

    def __init__(self, bus):
        self.bus = bus
        self.instances = {}

    async def start(self):
        while True:
            await asyncio.sleep(60)

    async def update_instance(self, instance_id, instance_type, mods):
        self.instances[instance_id] = {
            "type": instance_type,
            "mods": mods
        }

        await self.bus.publish("instances_updated", self.instances)
