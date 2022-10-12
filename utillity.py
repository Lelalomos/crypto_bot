import pandas as pd
import json
from pathlib import Path
from shutil import rmtree

def get_close_history(client, config)-> pd.DataFrame:
    """

    Args:
        config (dictionary): should have symbol, interval, starttime
        client (binance.client): client of binance

    Returns:
        dataframe : all close price data
        
    """

    bars = client.get_historical_klines(config["symbol"], config["interval"], config["starttime"])
    bars = [line[2:5] for line in bars]
    return pd.DataFrame(bars, columns=['hight','low','close'])


def ichimoku_cloud(df,tenkansen_value = 9, kinjunsen_value = 26, shift_value = 26, senkou_b_value = 52):
        """
        Description:
            Get the values of Lines for Ichimoku Cloud

        Args:
            df: Dataframe,
            int: tenkansen value,
            int: kinjunsen value,
            int: shift value,
            int: senkou_b value,

        Returns:
            df: Dataframe

        Reference Code: https://stackoverflow.com/questions/28477222/python-pandas-calculate-ichimoku-chart-components
        
        """

        # Tenkan-sen (Conversion Line): (9-period high + 9-period low)/2))
        period9_high = df['hight'].rolling(window=tenkansen_value).max()
        period9_low = df['low'].rolling(window=tenkansen_value).min()
        tenkan_sen = (period9_high + period9_low) / 2

        # Kijun-sen (Base Line): (26-period high + 26-period low)/2))
        period26_high = df['hight'].rolling(window=kinjunsen_value).max()
        period26_low = df['low'].rolling(window=kinjunsen_value).min()
        kijun_sen = (period26_high + period26_low) / 2

        # Senkou Span A (Leading Span A): (Conversion Line + Base Line)/2))
        senkou_span_a = ((tenkan_sen + kijun_sen) / 2).shift(shift_value)

        # Senkou Span B (Leading Span B): (52-period high + 52-period low)/2))
        period52_high = df['hight'].rolling(window=senkou_b_value).max()
        period52_low = df['low'].rolling(window=senkou_b_value).min()
        senkou_span_b = ((period52_high + period52_low) / 2).shift(shift_value)

        df['cloud_green_line_a'] = senkou_span_a
        df['cloud_red_line_b'] = senkou_span_b
        return df

def buy(price_play, logger, client, symbol_v, symbol_stable):
    """ _summary_

    Args:
        price_play (str): price for buy
        logger (logging): logging variable for log process
        client (client): client variable for connect binance host

    """
 
    if float(price_play) >= float(client.get_asset_balance(asset=symbol_stable)):
        logger.info('[PROCESS] BUY PRICE: %s', price_play)
        order_buy = client.order_market_buy(symbol=symbol_v, quoteOrderQty=price_play)
        logger.info('[DONE] CURRENT PRICE %s', client.get_asset_balance(asset=symbol_stable))
        logger.info('[DONE] INFORMATION %s', order_buy)
    else:
        logger.info('[FAIL] PRICE NOT ENOUGH')


def sell(price_original, price_sell, close_price, logger, client, symbol_v, symbol_stable):
    """ _summary_

    Args:
        price_original (str): free value of crypto (get value from price_original key in config)
        price_sell (str): free value of crypto (get current value of crypto)
        close_price (str): close price
        logger (logging): logging variable for log process
        client (client): client variable for connect binance host
        symbol_v (str): symbol for sell --> BTCBUSD
        symbol_stable (str): symbol for get price --> BUSD

    """

    price_original = float(price_original)
    price_sell = float(price_sell)
    close_price = float(close_price)
    sell_price = (max(price_original,price_sell) - min(price_original,price_sell))*close_price
    logger.info('[PROCESS] SELL PRICE: %s', sell_price)
    order_sell = client.order_market_sell(symbol=symbol_v, quoteOrderQty= str(sell_price))
    logger.info('[DONE] CURRENT PRICE %s', client.get_asset_balance(asset=symbol_stable))
    logger.info('[DONE] INFORMATION %s', order_sell)


def read_config(path_json):
    """

    Args:
        path_json (string): path json file

    Returns:
        dictionary: data of json file

    """
    with open(path_json) as js:
        return json.load(js)


def remove_file(path_file):
    """

    Args:
        path_json (string): path file

    """
    file_to_rem = Path(path_file)
    file_to_rem.unlink(missing_ok=True)

def remove_folder(path_folder):
    """

    Args:
        path_json (string): path folder

    """
    rmtree(path_folder,ignore_errors=True)