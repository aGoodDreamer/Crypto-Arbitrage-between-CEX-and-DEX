
import api
import time
import redis
import config
import multiprocessing as mp
base = config.baseName
r = redis.Redis(host='localhost',port=6379)
def main():
    while True:
        time.sleep(0.5)###
        while True:
            cexBaseBalance = float(r.get('cexBaseBalance'))
            cexQuoteBalance = float(r.get('cexQuoteBalance'))
            dexBaseBalance = float(r.get('dexBaseBalance'))
            dexQuoteBalance = float(r.get('dexQuoteBalance'))
            cexBuyPrice = float(r.get(base+'AskPrice'))
            cexSellPrice = float(r.get(base+'BidPrice'))
            dexBuyPrice = float(r.get('dexBuyPrice'))
            dexSellPrice = float(r.get('dexSellPrice'))
            break
        buyOrderAmount = config.maxOrderAmount
        sellOrderAmount = config.maxOrderAmount
        buyOrderAmount = min(buyOrderAmount,dexBaseBalance,dexBaseBalance/cexBuyPrice)
        sellOrderAmount = min(sellOrderAmount,dexQuoteBalance/cexBuyPrice * 0.99, cexBaseBalance)

        #cexBuyProfit = (dexSellPrice-cexBuyPrice)/(cexBuyPrice+dexSellPrice)/2#cex buy
        #cexSellProfit = (cexSellPrice-dexBuyPrice)/(dexBuyPrice+cexSellPrice)/2#cex sell
        cexBuyProfit = (dexSellPrice/cexBuyPrice)-1
        cexSellProfit = (cexSellPrice/dexBuyPrice)-1
        currentBase = dexBaseBalance + cexBaseBalance
        currentQuote = dexQuoteBalance + cexQuoteBalance
        timeNow = time.asctime()
        print(f'当前时间：{timeNow}\n',f'持币总量：{currentBase}\n',f'美元总量：{currentQuote}')
        print(f'买价差：{cexBuyProfit},卖价差：{cexSellProfit}')

        if cexBuyProfit > config.buyProfit  and buyOrderAmount > config.minOrderAmount:#dex卖，cex买
            api.sellCoins(amountIn=buyOrderAmount)
            api.buy_coins_limit(price=cexBuyPrice,amount=buyOrderAmount)
            time.sleep(10)
            
        if cexSellProfit > config.sellProfit and sellOrderAmount > config.minOrderAmount:#dex买，cex卖
            api.buyCoins(amountOut=sellOrderAmount)
            api.sell_coins_limit(price=cexSellPrice,amount=sellOrderAmount)
            time.sleep(10)
            
        print('----------------')

if __name__ == '__main__':
    m1 = mp.Process(target=main)
    m2 = mp.Process(target=api.modifyOrder)
    m1.start()
    m2.start()
    m1.join()
    m2.join()


'''
if cexBaseBalance and cexQuoteBalance and dexQuoteBalance and cexSellPrice and cexSellPrice and dexBuyPrice and dexSellPrice  and dexBaseBalance:
break
'''