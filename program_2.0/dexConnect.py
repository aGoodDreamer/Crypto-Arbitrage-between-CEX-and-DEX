import asyncio
from web3 import Web3
import config
import logging

provider = config.provider
web3 = Web3(Web3.HTTPProvider(provider))
contract_instance = web3.eth.contract(address = config.DexContractAddr, abi = config.DexABI)
#-------

file_handler = logging.FileHandler('app.log', mode='a', encoding='utf-8')
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger = logging.getLogger()
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)
#-----



async def get_price_from_dex():
    try:
        sPrice = await sell_price()
        bPrice = await purchase_price()
        return bPrice,sPrice
    except Exception as e:
        logging.error('DEX Price数据发生错误',e)
        return None
    

async def purchase_price(path=config.buyPath,amount=config.singlePurchasingMax,baseDecimals=config.baseDecimals,quotaDecimals=config.quotaDecimals):
    amountOut= amount * 10 ** baseDecimals
    inAmount = contract_instance.functions.getAmountsIn(amountOut,path).call()
    return inAmount[0]/10**quotaDecimals/amount



async def sell_price(path=config.sellPath,amount=config.singlePurchasingMax,baseDecimals=config.baseDecimals,quotaDecimals=config.quotaDecimals):
    amountIn= amount * 10 ** baseDecimals
    outAmount = contract_instance.functions.getAmountsOut(amountIn,path).call()
    return outAmount[-1]/10**quotaDecimals/amount
'''
async def main():
    while True:
        bp = await purchase_price()
        sp = await sell_price()
        print(f'Buy price is {bp}\nSell price is {sp}\n-----------')

asyncio.run(main())
'''