class EventBus:
    def __init__(self):
        self.listeners = {}

    def subscribe(self, event, callback):
        self.listeners.setdefault(event, []).append(callback)

    async def publish(self, event, data):
        for cb in self.listeners.get(event, []):
            await cb(data)
