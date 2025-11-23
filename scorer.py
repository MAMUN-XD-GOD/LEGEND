def compose_confidence(signal):
    c = signal.get('confidence', 50)
    return max(0, min(100, c))
