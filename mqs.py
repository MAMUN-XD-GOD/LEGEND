def score_pair(candles):
    if not candles:
        return 0
    spikes = 0
    for i in range(1, len(candles)):
        if abs(candles[i]['close'] - candles[i-1]['close'])/max(1, abs(candles[i-1]['close'])) > 0.003:
            spikes += 1
    spike_rate = spikes / len(candles)
    vols = [abs(c['high'] - c['low']) for c in candles]
    vol = sum(vols)/len(vols)
    score = max(0, 100 - spike_rate*100 - vol*1000)
    return score
