from web3 import Web3
import config
import info
import time
import redis

r = redis.Redis(host='localhost',port=6379)

baseAddr = info.baseAddr
quoteAddr = info.quoteAddr
buyPath = info.buyPath
sellPath = info.sellPath


provider = 'https://bsc-dataseed.binance.org/'
web3 = Web3(Web3.HTTPProvider(provider))
contract_instance = web3.eth.contract(address = info.contract_address, abi = info.contract_abi)



def fetch_buy_price(path=buyPath, getAmount=config.maxOrderAmount, decimals = 18):
    amountIn= int(getAmount * 10 ** decimals)
    amount = contract_instance.functions.getAmountsIn(amountIn,path).call()
    return amount[0]/10**18/getAmount

def fetch_sell_price(path=sellPath,sellAmount=config.maxOrderAmount, decimals = 18):
    amountIn = int(sellAmount * 10 ** decimals)
    amount = contract_instance.functions.getAmountsOut(amountIn,path).call()
    return amount[1]/10**18/sellAmount

def fetch_base_balance(coinAddress = baseAddr,decimals = 18):
    coin_init = web3.eth.contract(address=coinAddress, abi = info.coins_abi)
    coin_balance = coin_init.functions.balanceOf(account = info.account).call()
    return coin_balance/(10**decimals)

def fetch_quote_balance(coinAddress = quoteAddr,decimals = 18):
    coin_init = web3.eth.contract(address=coinAddress, abi = info.coins_abi)
    coin_balance = coin_init.functions.balanceOf(account = info.account).call()
    return coin_balance/(10**decimals)


while True:
    r.set('dexBuyPrice',fetch_buy_price(),ex=60)
    r.set('dexSellPrice',fetch_sell_price(),ex=60)
    r.set('dexBaseBalance',fetch_base_balance(),ex=60)
    r.set('dexQuoteBalance',fetch_quote_balance(),ex=60)
    time.sleep(1)