import json
class SignalManager:
    def __init__(self, db=None, path='signals.log'):
        self.db = db; self.path = path
    async def save(self, signal):
        with open(self.path, 'a') as f:
            f.write(json.dumps(signal) + '\n')
        if self.db:
            try:
                await self.db.insert_signal(signal)
            except Exception:
                pass
    async def save_many(self, signals):
        for s in signals:
            await self.save(s)
