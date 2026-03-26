import asyncio

class ComparisonEngine:

    def __init__(self, bus, ws):
        self.bus = bus
        self.ws = ws
        self.instances = {}

        self.bus.subscribe("instances_updated", self.on_instances)

    async def on_instances(self, instances):
        self.instances = instances

    async def start(self):
        while True:

            if "server" not in self.instances or "client" not in self.instances:
                await asyncio.sleep(5)
                continue

            server = self.instances["server"]["mods"]
            client = self.instances["client"]["mods"]

            server_map = {m["mod_id"]: m for m in server}
            client_map = {m["mod_id"]: m for m in client}

            missing_on_server = list(client_map.keys() - server_map.keys())
            missing_on_client = list(server_map.keys() - client_map.keys())

            version_mismatch = []

            for mod_id in server_map:
                if mod_id in client_map:
                    if server_map[mod_id].get("version") != client_map[mod_id].get("version"):
                        version_mismatch.append(mod_id)

            result = {
                "missing_on_server": missing_on_server,
                "missing_on_client": missing_on_client,
                "version_mismatch": version_mismatch
            }

            await self.bus.publish("comparison", result)

            if self.ws:
                await self.ws.broadcast({
                    "type": "comparison",
                    "data": result
                })

            await asyncio.sleep(10)
