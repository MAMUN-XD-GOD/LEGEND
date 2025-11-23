from backend.feature_engine import compute_features
from backend.smc_engine import detect_structure
from backend.multi_tf_gate import gate
from backend.spike_filter import is_spike
from backend.mqs import score_pair

class StrategyEngine:
    def __init__(self, db=None):
        self.db = db
    async def start(self):
        pass
    async def stop(self):
        pass
    async def evaluate(self, pair, candles):
        if not candles or len(candles) < 30:
            return None
        main = candles[-60:] if len(candles) >= 60 else candles
        short = candles[-15:]
        f_main = compute_features(main)
        f_short = compute_features(short)
        # MQS
        quality = score_pair(main)
        if quality < 25:
            return None
        # spike
        if is_spike(short):
            return None
        # gate
        if not gate(f_short, f_main):
            return None
        struct = detect_structure(main)
        direction = None; conf = 0; reasons = []
        if f_short.get('ema9') > f_short.get('ema21') and struct.get('bias') == 'bull':
            direction = 'CALL'; conf += 60; reasons.append('ema+structure')
        if f_short.get('ema9') < f_short.get('ema21') and struct.get('bias') == 'bear':
            direction = 'PUT'; conf += 60; reasons.append('ema+structure')
        if f_main.get('rsi') and (f_main.get('rsi') > 70 or f_main.get('rsi') < 30):
            conf -= 10; reasons.append('rsi_extreme')
        if direction and conf >= 40:
            return {'fire': True, 'signal': {'pair': pair, 'direction': direction, 'confidence': conf, 'reasons': reasons}}
        return None
