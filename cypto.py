from binance.client import Client
import os
import json
from binance import ThreadedWebsocketManager
import numpy as np

# get key api
api_key = os.environ.get('binance_api')
api_secret = os.environ.get('binance_secret')

data = {
    "price_buy":[],
    "price_sell":[],
    "price":0,
    "status":True,
    "sell":0,
    "sw":True,
    "first":True,
    "symbol":"ETHBUSD",
    "symbol_play": "ETH",
    "back_price": np.array([]),
    "price_play":15,
    "fee": 0.0075
}
client = Client(api_key, api_secret)
dict_data = {'error':False}
bsm = ThreadedWebsocketManager()

def btc_trade_history(msg):
    global data,bsm

    if data['status'] != True:
        print('save data')
        with open("data.json", "w+") as outfile:
            data['back_price'] = data['back_price'].tolist()
            json.dump(data, outfile)
        bsm.stop()
        
    if msg['e'] != 'error':
        if data['first']:
            # data['back_price'] = np.append(data['back_price'],float(msg['c']))
            # if len(data['back_price']) == 10:
            # print('initial app and prepare data')
            data["price"] = msg['c']
            data['first'] = False
            data['sw'] = False
        else:
            
            # delete first index in array
            # data['back_price'] = np.delete(data['back_price'], 0)
#           add new data to array
            # data['back_price'] = np.append(data['back_price'],float(msg['c']))

            # print("std:",np.std(data['back_price']))
            # std = np.std(data['back_price'])
            
#             len_bprice = len(data['back_price'])
#             positive_prob = 0
#             for i in range(len_bprice):
#                 cur_var = data['back_price'][i]
#                 try:
#                     curp1_var = data['back_price'][i+1]
#                     if cur_var < curp1_var:
#                         positive_prob+=1 
#                 except IndexError:
#                     break
                
#             # positive_prob = np.sum(prob_back_number)
#             negative_prob = len_bprice - positive_prob
#             check_prob = True # true:positive, false:nagative
#             if positive_prob < negative_prob:
#                 check_prob = False
            
#             print('check_prob:',check_prob)
            if data['sw']:
                data['price'] = float(data['price'])
                msg['c'] = float(msg['c'])
                if float(msg['c']) > float(data['price']):
                    data['price'] = max(data['price'],float(msg['c']))
                    

                if float(msg['c']) < data['price']:
                    max_var = max(data['price'],msg['c'])
                    min_var = min(data['price'],msg['c'])
                    percent_sell = ((max_var-min_var)/min_var)*100
                    # print("percent sell:",percent_sell)
                    if percent_sell > 0.05 and msg['c'] > data['sell']:
                        # sell
                        sell_price = client.get_asset_balance(asset=data['symbol_play']).get('free')
                        print('sell price',round(float(sell_price),4))
                        order_sell = client.order_market_sell(symbol=data['symbol'],quantity=round(float(sell_price),4))
                        # print('order_sell:',order_sell)
                        data["price_sell"].append(msg['c'])
                        # save price sell
                        data['price'] = msg['c']
                        print('sell:',data['price'])
                        # change status sw to False
                        data['sw'] = False

                    # if data['price'] >= data['price_buy'][-1]: 
                    #     max_sell_acc = max(data["price"],msg['c'])
                    #     min_sell_acc = min(data["price"],msg['c'])
                    #     percent_sell_acc = ((max_sell_acc-min_sell_acc)/min_sell_acc)*100
                    #     if percent_sell_acc >=0.001 and msg['c'] > data['sell'] and std < 0.51:
                    #         # sell_price = data["earn_coin"]+round((msg['c'] -  data['price_buy'][-1]),2)
                    #         sell_price = client.get_asset_balance(asset=data['symbol_play']).get('free')
                    #         print('sell price',round(float(sell_price),4))
                    #         order_sell = client.order_market_sell(symbol=data['symbol'],quantity=round(float(sell_price),4))
                    #         # print('order_sell:',order_sell)
                    #         data["price_sell"].append(msg['c'])
                    #         data['price'] = msg['c']
                    #         print('sell:',data['price'])
                    #         data['sw'] = False

            else:
                msg['c'] = float(msg['c'])
                data['price'] = float(data['price'])
                if data['price'] > msg['c']:
                    data['price'] = min(data['price'],msg['c'])

                if msg['c'] > data['price']:
                    max_var = max(data['price'],msg['c'])
                    min_var = min(data['price'],msg['c'])
                    percent_buy = ((max_var-min_var)/min_var)*100
                    # print("percent buy:",percent_buy)
                    if percent_buy > 0.05:
                        buy_coin = round(data["price_play"]/msg['c'],4)
                        print("buy_coin:",buy_coin)
                        order_buy = client.order_market_buy(symbol=data['symbol'],quantity=buy_coin)
                        coin_fee = msg['c']+(buy_coin*data['fee'])
                        data["price_buy"].append(coin_fee)
                        print('buy:',coin_fee)
                        data["price"] = float(msg['c'])
                        data['sell'] = coin_fee
                        data['sw'] = True
                    
        dict_data['last'] = msg['c']
        dict_data['bid'] = msg['b']
        dict_data['last'] = msg['a']
        dict_data['error'] = False
    else:
        dict_data['error'] = True

def stop_service():
    global data
    data['status'] = False

def main():
    bsm.start()
    print('starting ...... ')
    bsm.start_symbol_ticker_socket(callback=btc_trade_history, symbol=data["symbol"])