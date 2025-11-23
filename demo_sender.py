import asyncio, websockets, json, random, time

async def run():
    uri = 'ws://127.0.0.1:8765/ws/bridge'
    async with websockets.connect(uri) as ws:
        token = 'demo-token'
        pair = 'EURUSD'
        while True:
            ts = int(time.time())
            o = round(random.uniform(1.0800,1.0900),5)
            h = round(o + random.uniform(0,0.0010),5)
            l = round(o - random.uniform(0,0.0010),5)
            c = round(random.uniform(l,h),5)
            vol = random.randint(1,100)
            payload = {'token':token,'pair':pair,'candles':[{'ts':ts,'open':o,'high':h,'low':l,'close':c,'volume':vol}]}
            await ws.send(json.dumps(payload))
            resp = await ws.recv()
            print('sent, resp', resp)
            await asyncio.sleep(1)

if __name__ == '__main__':
    asyncio.run(run())
