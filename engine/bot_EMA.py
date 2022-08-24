import pandas as pd
import cache_memory
import re
from talib.abstract import EMA

class bot_EMA:
    def __init__(self, df, bot_name) -> None:
        self.df = df
        self.data = cache_memory.cache_manager(bot_name)

    def buyORsell(self, ema_low, ema_hight):
    #     buy 100>200
        if ema_low[-1] > ema_hight[-1]:
            return 0 #False
    #     sell 100<200
        elif ema_low[-1] < ema_hight[-1]:
            return 1 #True
        return 3

    def process(self, msg):
        if self.data.get_values('first'):
            self.data.update('first',False)
            self.data.update('p_open',msg['k']['o'])
            print('p_open:',msg['k']['o'])
        else:
            if float(msg['k']['o']) != float(self.data.get_values('p_open')):
                # state change 
                print('state change:',self.data.get_values('p_open'))
                self.df = self.df.iloc[1: , :]
                df2 = pd.DataFrame([msg['k']["o"]],columns=['close'])
                self.df = pd.concat([self.df, df2], ignore_index = True, axis = 0)

            if float(msg['k']['o']) != float(self.data.get_values('p_open')) or self.data.get_values('first'):
                # low_df = cal_EMA(self.df,self.data.get_values('low_span'))
                # hight_df = cal_EMA(self.df,self.data.get_values('hight_span'))
                low_df = EMA(self.df['close'],self.data.get_values('low_span'))
                hight_df = EMA(self.df['close'],self.data.get_values('hight_span'))
                sORb = self.buyORsell(low_df, hight_df)

                # sell
                if self.data.get_values('sw'):
                    # print('sell')
                    # check price sell>buy
                    if sORb:
                        split_price_buy = re.findall(r'\d+\.\d+|\d+',self.data.get_values('price_buy'))
                        if float(msg['k']['o']) > float(split_price_buy[-1]):
                            # order_sell = client.order_market_sell(symbol=data['symbol'],quantity=round(float(sell_price),4))
                            # print('order_sell:',order_sell)
                            self.data.update_sell(str(msg['k']['o']))
                            # save price sell
                            self.data.update('price',msg['k']['o'])
                            print('sell:',msg['k']['o'])
                            # change status sw to False
                            self.data.update('sw',False)
                            print('sw',self.data.get_values('sw'))
                # buy
                else:
                    # print('buy')
                    if not sORb:
                        # order_buy = client.order_market_buy(symbol=data['symbol'],quantity=buy_coin)
                        self.data.update_buy(str(msg['k']['o']))
                        print('buy:',msg['k']['o'])
                        # data["price"] = float(msg['k']['c'])
                        self.data.update('sw',True)
                        print('sw',self.data.get_values('sw'))
                        
                # change value
                self.data.update('p_open',msg['k']['o'])
                print('changed:',self.data.get_values('p_open'))