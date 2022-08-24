from binance.client import Client
import os
from binance import ThreadedWebsocketManager
from utillity import read_config, get_close_history

# bot version
# from engine.bot_MACD import bot_MACD
from engine.bot_EMA import bot_EMA


import cache_memory

api_key = os.environ.get('binance_api')
api_secret = os.environ.get('binance_secret')

print('api_key:',api_key)
print('api_secret:',api_secret)

main_config = read_config(os.path.join(os.getcwd(),'main_config','main_config.json'))
client = Client(api_key, api_secret)
dict_data = {'error':False}
bsm = ThreadedWebsocketManager()
bot_name = "botv3"
data = cache_memory.cache_manager(bot_name)
data.init_data(os.path.join(os.getcwd(),'bot_config',f'{bot_name}.json'))
print('prepare data')
df = get_close_history(client,data.get_all_data())
print('finish')
bot = bot_EMA(df, bot_name)

def btc_trade_history(msg):
    global bsm, bot
    if data.get_values('status') != True:
        try:
            bsm.stop()
        except KeyError:
            print('stopped')

    if msg['e'] != 'error':
        # read config
        bot.process(msg)
        dict_data['error'] = False
    else:
        dict_data['error'] = True
        

def stop_service():
    data.clear_data()
    data.update('status',False)

def main():
    bsm.start()
    print('starting ...... ')
    bsm.start_kline_futures_socket(callback=btc_trade_history, symbol=data.get_values("symbol"),interval=data.get_values("interval"))