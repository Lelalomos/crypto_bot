import pandas as pd
import cache_memory
import re
from utillity import ichimoku_cloud, buy, sell

class bot_ichimoku:
    def __init__(self, df, bot_name, logger, client) -> None:
        self.df = df
        self.logger = logger
        self.client = client
        self.data = cache_memory.cache_manager(bot_name)

    def buyORsell(self):
        
        close = self.df['close'].to_list()[-1]
        cloud_green_line_a = self.df['cloud_green_line_a'].to_list()[-1]
        cloud_red_line_b = self.df['cloud_red_line_b'].to_list()[-1]

        close = float(close)
        cloud_green_line_a = float(cloud_green_line_a)
        cloud_red_line_b = float(cloud_red_line_b)

        # buy
        if close > cloud_green_line_a and close > cloud_red_line_b and cloud_green_line_a > cloud_red_line_b:
            return 0
        # sell
        elif close < cloud_green_line_a and close < cloud_red_line_b and cloud_green_line_a < cloud_red_line_b:
            return 1
        # noting
        else:
            return 3

    def process(self, msg):
        if self.data.get_values('first'):
            self.data.update('first',False)
            self.data.update('p_open',msg['k']['o'])
            self.logger.info("[PROCESS] INIT PRICE %s",msg['k']['o'])
        else:
            if float(msg['k']['o']) != float(self.data.get_values('p_open')):
                # state change 
                self.logger.info("[PROCESS] PRICE CHANGE %s",self.data.get_values('p_open'))
                self.df = self.df.iloc[1: , :]
                df2 = pd.DataFrame({'hight':float(msg['k']['h']), 'low':float(msg['k']['l']), 'close':float(msg['k']['c'])},index=[0])
                self.df = pd.concat([self.df, df2], ignore_index = True, axis = 0)

            if float(msg['k']['o']) != float(self.data.get_values('p_open')) or self.data.get_values('first'):

                self.df = ichimoku_cloud(self.df, self.data.get_values('tenkansen'), self.data.get_values('kinjunsen'), self.data.get_values('shift'), self.data.get_values('senkou_b'))
                sORb = self.buyORsell()

                # sell
                if self.data.get_values('sw'):
                    # print('sell')
                    # check price sell>buy
                    if sORb:
                        split_price_buy = re.findall(r'\d+\.\d+|\d+',self.data.get_values('price_buy'))
                        if float(msg['k']['c']) > float(split_price_buy[-1]):
                            
                            if self.data.get_values('accept2play'):
                                sell(self.data.get_values('price_original'), self.client.get_asset_balance(asset=self.data.get_values('symbol_stable')), msg['k']['c'], self.logger, self.client, self.data.get_values('symbol'), self.data.get_values('symbol_stable'))

                            self.data.update_sell(str(msg['k']['c']))
                            # save price sell
                            self.data.update('price',msg['k']['c'])
                            self.logger.info('[DO] SELL: %s', msg['k']['c'])
                            # change status sw to False
                            self.data.update('sw',False)
                            # print('sw',self.data.get_values('sw'))
                # buy
                else:
                    # print('buy')
                    if not sORb:

                        if self.data.get_values('accept2play'):
                            buy(self.data.get_values('price_play'), self.logger, self.client, self.data.get_values('symbol'),self.data.get_values('symbol_stable'))

                        self.data.update_buy(str(msg['k']['c']))
                        self.logger.info('[DO] BUY: %s',msg['k']['c'])
                        # data["price"] = float(msg['k']['c'])
                        self.data.update('sw',True)
                        # print('sw',self.data.get_values('sw'))
                        
                # change value
                self.data.update('p_open',msg['k']['o'])
                # print('changed:',self.data.get_values('p_open'))