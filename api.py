import ccxt
from web3 import Web3
import config
import info
import redis

r = redis.Redis(host='localhost',port=6379)
base = config.baseName
quote = config.quoteName
symbol = config.symbol
baseAddr = info.baseAddr
quoteAddr = info.quoteAddr
buyPath = info.buyPath
sellPath = info.sellPath

exchange = ccxt.huobi({
    'rateLimit' : 500,
    'enableRateLimit' : True,
    'timeout' : 15000,
    'apiKey' : info.cexApiKey,
    'secret' : info.cexApiSecret
})

def buy_coins_limit(symbol = symbol,price = None,amount = None):
    exchange.create_order(symbol=symbol,side='buy',type='limit',price=price,amount=amount)

def sell_coins_limit(symbol = symbol,price = None,amount = None):
    exchange.create_order(symbol=symbol,side='sell',type='limit',price=price,amount=amount)

def fetch_order_id():
    return exchange.fetch_open_orders(symbol = symbol)[-1]['id']

def cancel_order(orderId,symbol=symbol):
    exchange.cancel_order(id=orderId,symbol=symbol)

'''
async def modify_order():
    await 
    '''

'''
def modifySellOrder():
        orders = exchange.fetch_open_orders(symbol=symbol)
        if len(orders)==0:
            pass
        else:
            orderId = orders[-1]['id']
            time.sleep(60*5)
            orders = exchange.fetch_open_orders(symbol=symbol)
            for order in orders:
                if order['id'] == orderId:
                    exchange.cancel_order(orderId=orderId,symbol=symbol)
                    new_amount = order['remaining']
                    new_price = float(r.get(base+'BidPrice'))
                    sell_coins_limit(symbol = symbol,price = new_price,amount=new_amount)
                    modifySellOrder()


def modifyBuyOrder():
    orders = exchange.fetch_open_orders(symbol=symbol)
    if len(orders)==0:
        pass
    else:
        orderId = orders[-1]['id']
        time.sleep(60*5)
        orders = exchange.fetch_open_orders(symbol=symbol)
        for order in orders:
            if order['id'] ==orderId:
                exchange.cancel_order(orderId = orderId,symbol = symbol)
                new_amount = order['remaining']
                new_price = float(r.get(base+'AskPrice'))
                buy_coins_limit(symbol=symbol,price=new_price,amount=new_amount)
                modifyBuyOrder()
                '''

def modifyOrder():
    while True:
        import time
        time.sleep(30)
        orders = exchange.fetch_open_orders(symbol=symbol)
        if len(orders)==0:
            pass
        elif orders[-1]['side'] == 'buy':
            orderId = orders[-1]['id']
            time.sleep(60*5)
            orders = exchange.fetch_open_orders(symbol=symbol)
            for order in orders:
                if order['id'] == orderId:
                    exchange.cancel_order(orderId=orderId,symbol=symbol)
                    new_amount = order['remaining']
                    new_price = float(r.get(base+'BidPrice'))
                    sell_coins_limit(symbol = symbol,price = new_price,amount=new_amount)
                    modifyOrder()
        elif orders[-1]['side'] == 'sell':
            orderId = orders[-1]['id']
            time.sleep(60*5)
            orders = exchange.fetch_open_orders(symbol=symbol)
            for order in orders:
                if order['id'] == orderId:
                    exchange.cancel_order(orderId=orderId,symbol=symbol)
                    new_amount = order['remaining']
                    new_price = float(r.get(base+'BidPrice'))
                    sell_coins_limit(symbol = symbol,price = new_price,amount=new_amount)
                    modifyOrder()

provider = 'https://bsc-dataseed.binance.org/'
web3 = Web3(Web3.HTTPProvider(provider))
contract_instance = web3.eth.contract(address = info.contract_address, abi = info.contract_abi)

def sellCoins(path=sellPath,amountIn = 0, sellAmountMin = 0):
    import time
    amountIn=int(amountIn*10**18)
    amountOutMin=int(sellAmountMin*10**18)
    to = info.account
    timeNow = time.time()
    deadline = int(timeNow + 20*60*1000)
    data = contract_instance.encodeABI(fn_name='swapExactTokensForTokens', args=[
        amountIn,
        amountOutMin,
        path,
        to,
        deadline
        ])
    nonce = web3.eth.getTransactionCount(info.account)

    tx = {
        'nonce' : nonce,
        'chainId': 56,
        'to' : info.contract_address,
        'data' : data,
        'gasPrice': web3.toWei(config.gasPrice,'gwei'),
        'gas': config.gas
        }

    signed_tx = web3.eth.account.sign_transaction(tx,info.private_key)
    web3.eth.send_raw_transaction(signed_tx.rawTransaction)

def buyCoins(path = buyPath ,amountOut  = 0, amountInMax = 200):
    import time
    amountOut = int(amountOut*10**18)
    amountInMax = int(amountInMax*10**18)
    to = info.account
    timeNow = time.time()
    deadline = int(timeNow + 200*60*1000)
    data = contract_instance.encodeABI(fn_name='swapTokensForExactTokens',args=[
        amountOut,
        amountInMax,
        path,
        to,
        deadline
    ]) 
    nonce = web3.eth.getTransactionCount(info.account)

    tx = {
        'nonce' : nonce,
        'chainId': 56,
        'to' : info.contract_address,
        'data' : data,
        'gasPrice': web3.toWei(config.gasPrice,'gwei'),
        'gas': config.gas
        }

    signed_tx = web3.eth.account.sign_transaction(tx,info.private_key)
    web3.eth.send_raw_transaction(signed_tx.rawTransaction)