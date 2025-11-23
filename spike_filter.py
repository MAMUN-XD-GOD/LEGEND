def is_spike(candles, threshold=0.003):
    if len(candles) < 2:
        return False
    last = candles[-1]['close']
    prev = candles[-2]['close']
    if prev == 0:
        return False
    if abs(last - prev)/abs(prev) > threshold:
        return True
    return False
