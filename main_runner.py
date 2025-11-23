"""Main runner: starts DataFeed, StrategyEngine, SignalManager, and a minute scheduler.
Run: python backend/main_runner.py
"""
import asyncio, logging
from backend.data_feed import DataFeed
from backend.strategy_engine import StrategyEngine
from backend.signal_manager import SignalManager
from backend.database import Database
from backend.scheduler import MinuteScheduler

logging.basicConfig(level=logging.INFO)
LOG = logging.getLogger('main_runner')

async def on_minute(ts, datafeed):
    engine = on_minute.engine
    signals_mgr = on_minute.signals
    df = datafeed.get_all_candles()
    collected = []
    for pair, candles in df.items():
        decision = await engine.evaluate(pair, candles)
        if decision and decision.get('fire'):
            collected.append(decision['signal'])
    if collected:
        await signals_mgr.save_many(collected)
        for s in collected:
            LOG.info('Signal emitted: %s', s)

async def main():
    db = Database('trade_logs.db')
    await db.connect()
    datafeed = DataFeed(pairs=['EURUSD'])
    await datafeed.start()
    engine = StrategyEngine(db=db)
    await engine.start()
    signals = SignalManager(db=db)
    scheduler = MinuteScheduler(lambda ts: on_minute(ts, datafeed))
    on_minute.engine = engine
    on_minute.signals = signals
    await scheduler.start()
    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        await scheduler.stop(); await datafeed.stop(); await db.disconnect()

if __name__ == '__main__':
    asyncio.run(main())
