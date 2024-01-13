import ccxt.pro
from asyncio import run
import config
import logging

file_handler = logging.FileHandler('app.log', mode='a', encoding='utf-8')
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger = logging.getLogger()
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)

exchange = ccxt.pro.huobi({
    "apiKey": "",
    "secret": "",
    'emableRateLimit': True,
    'newUpdates': True,
    })

def write_log(message):
    with open('log.txt', 'a') as file:
        file.write(message + '\n')

async def get_price_from_cex():
    symbol = config.symbol
    try:
        orderbook = await exchange.watch_order_book(symbol)
        #print(orderbook['bids'][0], orderbook['asks'][0])
        return orderbook['bids'][config.orderBookBidNumber][0], orderbook['asks'][config.orderBookAskNumber][0]
    except Exception as e:
        logging.error('读取价格数据时发生错误',e)
        return None
    

async def get_balance():
    try:
        balance = await exchange.watch_balance()
        return balance[config.base]['free'], balance[config.quota]['free']
    except Exception as e:
        logging.error('获取余额时发生错误',e)
        return None