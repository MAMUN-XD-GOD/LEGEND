def detect_structure(candles):
    if len(candles) < 10:
        return {'bias':'neutral'}
    closes = [c['close'] for c in candles[-10:]]
    if closes[-1] > max(closes[:-1]):
        return {'bias':'bull'}
    if closes[-1] < min(closes[:-1]):
        return {'bias':'bear'}
    return {'bias':'neutral'}
