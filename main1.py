import ccxt
import time

import asyncio
import numpy as np
import itertools


bittrex = ccxt.bittrex({
    'enableRateLimit': True,  # this option enables the built-in rate limiter
    })

markets = bittrex.load_markets()
whichmarket = (bittrex.symbols)
coins_with_7_day = {}

f = 0

def now():
    return int(time.time() * 1000)
 
def count_consective(l):
    """Takes a list and returns number of consecutive positive numbers
   >>> count_consective([True, True, True])
   3
   >>> count_consective([False, True, False])
   1
   """
    m = 0
    for group, it in itertools.groupby(l):
        if group:
            m = max(len(list(it)), m)
    return m 

while f < len(whichmarket):
    try:
        ohlcv = ccxt.bittrex().fetch_ohlcv(whichmarket[f], '1d')
        prices = [(d[0], d[2]) for d in ohlcv]  # use high/open for candles
        prices = [prices[i] for i in range(0, len(prices), 7)]
        last_seven_weeks = sorted(prices, key=lambda x: x[0], reverse=True)[:3]
        offset = (now() - last_seven_weeks[0][0]) / (60 * 60 * 1000)
        print(f'{offset:.2f} hours since last candle')
        lsw_prices = np.array([i[1] for i in last_seven_weeks])
        diff = lsw_prices[:-1] - lsw_prices[1:]
        positive = diff > 0
        candles = count_consective(positive)
        print(f'{whichmarket[f]} {candles} consecutive green candle(s) in the last week')
        if candles >= 2:
            coins_with_7_day[whichmarket[f]] = candles
        f = f + 1
    except (ccxt.ExchangeError,ccxt.NetworkError,ccxt.RequestTimeout) as error: 
        print('Got an error', type(error).__name__, error.args) 
    time.sleep(0.5)
    continue           

coin_score = {}

for x in coins_with_7_day:
    if coins_with_7_day[x] == 2:
        coin_score[x] = 0.5
    else:
        coin_score[x] = 1
print (coins_with_7_day)
print (coin_score)