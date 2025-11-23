from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import json, logging, asyncio
app = FastAPI()
LOG = logging.getLogger('bridge_server')

@app.websocket('/ws/bridge')
async def bridge_ws(ws: WebSocket):
    await ws.accept()
    LOG.info('bridge client connected')
    try:
        while True:
            text = await ws.receive_text()
            try:
                payload = json.loads(text)
            except Exception:
                await ws.send_text(json.dumps({'error':'invalid_json'}))
                continue
            token = payload.get('token')
            if not token:
                await ws.send_text(json.dumps({'error':'no_token'}))
                continue
            pair = payload.get('pair')
            candles = payload.get('candles')
            if not pair or not candles:
                await ws.send_text(json.dumps({'error':'missing_fields'}))
                continue
            # safe: write normalized payload file for DataFeed to pick up
            fname = f'/tmp/quantum_bridge_{pair}.json'
            try:
                with open(fname, 'w') as f:
                    json.dump({'candles':candles, 'ts': int(asyncio.get_event_loop().time())}, f)
            except Exception:
                LOG.exception('write fail')
            await ws.send_text(json.dumps({'status':'ok'}))
    except WebSocketDisconnect:
        LOG.info('bridge disconnected')
