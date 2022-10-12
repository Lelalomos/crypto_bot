import pandas as pd
from talib.abstract import MACD, STOCH
import cache_memory
import re
from utillity import sell, buy

class bot_MACD_STOCH:
    def __init__(self, df, bot_name, logger, client):
        self.df = df
        self.logger = logger
        self.client = client
        self.data = cache_memory.cache_manager(bot_name)

    def buyORsell(self, macd_var, signal_var):
        #     buy
        if macd_var[-1]>signal_var[-1]:
            return 0 #False
        #     sell
        elif macd_var[-1]<signal_var[-1]:
            return 1 #True
        return 3

    def process(self,msg):
        if self.data.get_values('first'):
            self.data.update('first',False)
            self.data.update('p_open',msg['k']['o'])
            self.logger.info("[PROCESS] INIT PRICE %s",msg['k']['o'])
            # print('p_open:',msg['k']['o'])
        else:
            if float(msg['k']['o']) != float(self.data.get_values('p_open')):
                # state change 
                # print('state change:',self.data.get_values('p_open'))
                self.logger.info("[PROCESS] PRICE CHANGE %s",self.data.get_values('p_open'))
                self.df = self.df.iloc[1: , :]
                df2 = pd.DataFrame({'hight':float(msg['k']['h']), 'low':float(msg['k']['l']), 'close':float(msg['k']['c'])},index=[0])
                self.df = pd.concat([self.df, df2], ignore_index = True, axis = 0)
                    
            if float(msg['k']['o']) != float(self.data.get_values('p_open')) or self.data.get_values('first'):
                # calculate signal and MACD
                macd, signal, _ = MACD(self.df['close'])
                sORb = self.buyORsell(macd, signal)
                slowk, slowd = STOCH(self.df['hight'], self.df['low'], self.df['close'])

                # sell
                if self.data.get_values('sw'):
                    # print('sell')
                    # check price sell>buy
                    hight_stoch = int(self.data.get_values('hight_stoch'))
                    if sORb and slowk[-1] < slowd[-1] and slowk[-1] >= hight_stoch and slowd[-1] >= hight_stoch:
                        split_price_buy = re.findall(r'\d+\.\d+|\d+',self.data.get_values('price_buy'))
                        if float(msg['k']['c']) > float(split_price_buy[-1]):

                            if self.data.get_values('accept2play'):
                                sell(self.data.get_values('price_original'), self.client.get_asset_balance(asset=self.data.get_values('symbol_stable')), msg['k']['c'], self.logger, self.client, self.data.get_values('symbol'), self.data.get_values('symbol_stable'))

                            self.data.update_sell(str(msg['k']['c']))
                            # save price sell
                            self.data.update('price',msg['k']['c'])
                            self.logger.info('[DO] SELL: %s', msg['k']['c'])
                            # print('sell:',msg['k']['c'])
                            # change status sw to False
                            self.data.update('sw',False)
                            # print('sw',self.data.get_values('sw'))
                # buy
                else:
                    # print('buy')
                    low_stoch = int(self.data.get_values('low_stoch'))
                    if not sORb and slowk[-1] > slowd[-1] and slowk[-1] <= low_stoch and slowd[-1] <= low_stoch:
                        
                        if self.data.get_values('accept2play'):
                            buy(self.data.get_values('price_play'), self.logger, self.client, self.data.get_values('symbol'),self.data.get_values('symbol_stable'))

                        self.data.update_buy(str(msg['k']['c']))
                        # print('buy:',msg['k']['c'])
                        self.logger.info('[DO] BUY: %s',msg['k']['c'])
                        # data["price"] = float(msg['k']['c'])
                        self.data.update('sw',True)
                        # print('sw',self.data.get_values('sw'))
                        
                # change value
                self.data.update('p_open',msg['k']['o'])
                # print('changed:',self.data.get_values('p_open'))

        # print('config:',self.data.get_values('sw'))
        

    
