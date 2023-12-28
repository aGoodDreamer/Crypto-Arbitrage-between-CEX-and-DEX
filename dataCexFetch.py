import ccxt
import config
import redis
import time
import info

r = redis.Redis(host='localhost',port=6379)

quote = config.quoteName
exchange = ccxt.huobi({
    'enableRateLimit':True,
    'rateLimit':500,
    'timeout':15000,
    'apiKey':info.cexApiKey,
    'secret': info.cexApiSecret
    })
baseList = [config.baseName]
while True:

    quoteBalance = exchange.fetch_balance()[quote]['free']
    r.set('cexQuoteBalance',quoteBalance,60)
    for base in baseList:
        orderbook = exchange.fetch_order_book(base+'/'+quote)
        r.set(base+'BidPrice',orderbook['bids'][config.orderBookBidNumber][0],ex=60)
        r.set(base+'AskPrice',orderbook['asks'][config.orderBookAskNumber][0],ex=60)
        balance = exchange.fetch_balance()[base]['free']
        r.set('cexBaseBalance',balance,60)
    
    time.sleep(1)
