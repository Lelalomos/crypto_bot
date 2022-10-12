from binance.client import Client
import os
from binance import ThreadedWebsocketManager
from utillity import read_config, get_close_history, remove_file

# bot
from engine.bot_MACD import bot_MACD
from engine.bot_EMA_STOCH import bot_EMA_STOCH
from engine.bot_EMA import bot_EMA
from engine.bot_MACD_STOCH import bot_MACD_STOCH
from engine.bot_ichimoku import bot_ichimoku

# cache 
import cache_memory

# logging
import logging
logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# load config
keys = read_config(os.path.join(os.getcwd(),'config','key.json'))
main_config = read_config(os.path.join(os.getcwd(),'main_config','main_config.json'))

client = Client(keys["api_key"], keys['api_secret'])
dict_data = {'error':False}
bsm = ThreadedWebsocketManager()
bot_name = main_config['engine']
data = cache_memory.cache_manager(bot_name)
data.init_data(os.path.join(os.getcwd(),'bot_config',f'bot_{bot_name}.json'))

# save price
cprice = client.get_asset_balance(asset=data.get_values('symbol_stable'))
data.update('price_original',cprice)

logger.info('[PROCESS] PREPARE DATA')
df = get_close_history(client,data.get_all_data())
logger.info('[DONE] PREPARE DATA')

bot = eval(f"bot_{bot_name}")(df, bot_name, logger, client)

def btc_trade_history(msg):
    global bsm, bot

    if msg['e'] != 'error':
        try:
            bot.process(msg)
        except Exception:
            # print('error engine:',e)
            logger.error('[ERROR] ERROR ENGINE PROCESS', exc_info=True)
            bsm.stop()
            logger.info('[DONE] STOP ENGINE')

        dict_data['error'] = False
    else:
        dict_data['error'] = True
        bsm.stop()
        logger.info('[DONE] STOP ENGINE')

    if data.get_values('status') != True:
        bsm.stop()
        if main_config['end']['rmdata']:
            data.clear_data()
            remove_file(os.path.join(os.getcwd(),'cache',f'{bot_name}.sqlite'))
        
def stop_service():
    data.update('status',False)
    logger.info('[DONE] STOP ENGINE')
    # print('stop service')

def buy():
    pprice = data.get_values('price_play')
    if float(pprice) >= float(client.get_asset_balance(asset='BUSD')):
        logger.info('[PROCESS] PRICE: %s', pprice)
        order_buy = client.order_market_buy(symbol='BTCBUSD', quoteOrderQty=10)
        logger.info('[DONE] CURRENT PRICE %s', client.get_asset_balance(asset='BUSD'))
        logger.info('[DONE] INFORMATION %s', order_buy)
    else:
        logger.info('[FAIL] PRICE NOT ENOUGH')

def main():
    bsm.start()
    logger.info('[INIT] START ENGINE')
    bsm.start_kline_futures_socket(callback=btc_trade_history, symbol=data.get_values("symbol"),interval=data.get_values("interval"))