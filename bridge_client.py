"""Local Bridge client
- Demo mode: generates synthetic candles and sends to bridge server
- Real mode: placeholder where you integrate DOM/screenshot parser and call send_candles
"""
import asyncio, websockets, json, time

async def send_candles(uri, pair='EURUSD', token='demo-token'):
    async with websockets.connect(uri) as ws:
        while True:
            ts = int(time.time())
            o = 1.0800
            h = round(o + 0.0005, 5)
            l = round(o - 0.0005, 5)
            c = round(o + 0.0001, 5)
            vol = 1
            payload = {'token': token, 'pair': pair, 'candles': [{'ts': ts, 'open': o, 'high': h, 'low': l, 'close': c, 'volume': vol}]}
            await ws.send(json.dumps(payload))
            resp = await ws.recv()
            print('bridge_client sent, resp:', resp)
            await asyncio.sleep(1)

if __name__ == '__main__':
    asyncio.run(send_candles('ws://127.0.0.1:8765/ws/bridge'))
