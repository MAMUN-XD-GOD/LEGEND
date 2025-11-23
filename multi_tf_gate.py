def gate(short_feat, long_feat):
    if not short_feat or not long_feat:
        return False
    sd = 'bull' if short_feat.get('ema9',0) > short_feat.get('ema21',0) else 'bear'
    ld = 'bull' if long_feat.get('ema9',0) > long_feat.get('ema21',0) else 'bear'
    return sd == ld
