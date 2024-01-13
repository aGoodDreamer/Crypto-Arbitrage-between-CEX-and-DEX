import asyncio
import time
import cexConnect
import dexConnect
import config
import logging
#------------logging
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
'''
file_handler = logging.FileHandler('app.log', mode='a', encoding='utf-8')

file_handler.setFormatter(formatter)
logger = logging.getLogger()
logger.addHandler(file_handler)
logger.setLevel(logging.ERROR)
'''

handler = logging.FileHandler('data.log', mode='a', encoding='utf-8')
handler.setFormatter(formatter)
logger2 = logging.getLogger()
logger2.addHandler(handler)
logger2.setLevel(logging.INFO)
#----
bidsPrice = None
askPrice = None
buyPrice = None
sellPrice = None
taskCexPrices = None
taskDexPrices = None
#---


async def checkPriceDifference():
    global bidsPrice, askPrice,buyPrice, sellPrice,taskCexPrices,taskDexPrices

    while True:
        if taskCexPrices.done():
            bidsPrice, askPrice = taskCexPrices.result()
            taskCexPrices = asyncio.ensure_future(cexConnect.get_price_from_cex())
            
        if taskDexPrices.done():
            buyPrice, sellPrice = taskDexPrices.result()
            taskDexPrices = asyncio.ensure_future(dexConnect.get_price_from_dex())
            await asyncio.gather(taskDexPrices, taskCexPrices)
            
        #Caculate diff here
        triggerBuyinCex = config.triggerBuyinCex
        triggerSellinCex = config.triggerSellinCex
        cexBuyProfit = (sellPrice/bidsPrice)-1
        cexSellProfit = (askPrice/buyPrice)-1
        #monitor
        timeNow = time.asctime()
        print(f'Time: {timeNow}\n Var in purchasing: {cexBuyProfit}\n Var in selling: {cexSellProfit}\n ------------------')

        if cexBuyProfit > triggerBuyinCex:
           #await buyAndSell() 
            logger2.info(f'Buy in Cex, Sell in Dex, Var in purchasing is {cexBuyProfit}, in selling is {cexSellProfit}')
            await asyncio.sleep(120)
            await refresh()
            break
        if cexSellProfit > triggerSellinCex:
            #await sellAndBuy()
            logger2.info(f'Sell in Cex, Buy in Dex, Var in purchasing is {cexBuyProfit}, in selling is {cexSellProfit}')
            await asyncio.sleep(120)
            await refresh()
            break

async def refresh():
    global bidsPrice, askPrice,buyPrice, sellPrice,taskCexPrices,taskDexPrices
    taskDexPrices = asyncio.ensure_future(dexConnect.get_price_from_dex())
    taskCexPrices = asyncio.ensure_future(cexConnect.get_price_from_cex())
    await asyncio.gather(taskDexPrices, taskCexPrices)
    while not (taskDexPrices.done() and taskCexPrices.done()):
        await asyncio.sleep(0.5)


async def main():
    logger2.info('Start working...')
    global bidsPrice, askPrice,buyPrice, sellPrice,taskCexPrices,taskDexPrices
    taskDexPrices = asyncio.ensure_future(dexConnect.get_price_from_dex())
    taskCexPrices = asyncio.ensure_future(cexConnect.get_price_from_cex())
    await asyncio.gather(taskDexPrices, taskCexPrices)
    while not (taskDexPrices.done() and taskCexPrices.done()):
        await asyncio.sleep(1)
    bidsPrice, askPrice = taskCexPrices.result()
    buyPrice, sellPrice = taskDexPrices.result()
    while True:
        await checkPriceDifference()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt: 
        pass