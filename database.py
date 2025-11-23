import aiosqlite
class Database:
    def __init__(self, path='trade_logs.db'):
        self.path = path; self.conn = None
    async def connect(self):
        self.conn = await aiosqlite.connect(self.path)
        await self.conn.execute('''CREATE TABLE IF NOT EXISTS signals(id INTEGER PRIMARY KEY AUTOINCREMENT, pair TEXT, direction TEXT, confidence REAL, reasons TEXT, ts DATETIME DEFAULT CURRENT_TIMESTAMP)''')
        await self.conn.commit()
    async def insert_signal(self, signal):
        await self.conn.execute('INSERT INTO signals(pair,direction,confidence,reasons) VALUES(?,?,?,?)', (signal['pair'], signal['direction'], float(signal['confidence']), ','.join(signal.get('reasons',[]))))
        await self.conn.commit()
    async def disconnect(self):
        if self.conn:
            await self.conn.close()
