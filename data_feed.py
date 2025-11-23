import asyncio, os, json, logging
from collections import defaultdict, deque
LOG = logging.getLogger('data_feed')

class DataFeed:
    def __init__(self, pairs=None):
        self.pairs = pairs or ['EURUSD']
        self.buckets = defaultdict(lambda: deque(maxlen=2000))
        self._running = False

    async def start(self):
        self._running = True
        asyncio.create_task(self._loop())

    async def stop(self):
        self._running = False

    async def _loop(self):
        while self._running:
            try:
                for pair in self.pairs:
                    fname = f'/tmp/quantum_bridge_{pair}.json'
                    if os.path.exists(fname):
                        try:
                            with open(fname,'r') as f:
                                payload = json.load(f)
                            for c in payload.get('candles',[]):
                                self.buckets[pair].append(c)
                        except Exception:
                            LOG.exception('read fail')
            except Exception:
                LOG.exception('poll error')
            await asyncio.sleep(0.5)

    def get_candles(self, pair, limit=200):
        dq = self.buckets.get(pair)
        if not dq:
            return []
        return list(dq)[-limit:]

    def get_all_candles(self):
        return {p:list(dq) for p,dq in self.buckets.items()}
