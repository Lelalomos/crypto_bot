from binance.client import Client
import os
from binance import ThreadedWebsocketManager
from utillity import read_config, get_close_history, remove_file

# bot
from engine.bot_MACD import bot_MACD
from engine.bot_EMA_STOCH import bot_EMA_STOCH
from engine.bot_EMA import bot_EMA
from engine.bot_MACD_STOCH import bot_MACD_STOCH

import cache_memory

# load config
keys = read_config(os.path.join(os.getcwd(),'config','key.json'))
main_config = read_config(os.path.join(os.getcwd(),'main_config','main_config.json'))

client = Client(keys["api_key"], keys['api_secret'])
dict_data = {'error':False}
bsm = ThreadedWebsocketManager()
bot_name = main_config['engine']
data = cache_memory.cache_manager(bot_name)
data.init_data(os.path.join(os.getcwd(),'bot_config',f'bot_{bot_name}.json'))

print('prepare data')
df = get_close_history(client,data.get_all_data())
print('finish')

bot = eval(f"bot_{bot_name}")(df, bot_name)

def btc_trade_history(msg):
    global bsm, bot

    if msg['e'] != 'error':
        try:
            bot.process(msg)
        except Exception as e:
            print('error engine:',e)
            bsm.stop()

        dict_data['error'] = False
    else:
        dict_data['error'] = True
        bsm.stop()

    if data.get_values('status') != True:
        bsm.stop()
        if main_config['end']['rmdata']:
            data.clear_data()
            remove_file(os.path.join(os.getcwd(),'cache',f'{bot_name}.sqlite'))
        
def stop_service():
    data.update('status',False)
    print('stop service')

def main():
    bsm.start()
    print('starting ...... ')
    bsm.start_kline_futures_socket(callback=btc_trade_history, symbol=data.get_values("symbol"),interval=data.get_values("interval"))