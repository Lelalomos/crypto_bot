import pandas as pd
import json

def calculate_signal(df):
    """

    Args:
        df (dataframe): all data close price from binance or etc.

    Returns:
        dataframe: MACD values
        dataframe: signal values

    """
    # EMA 12 
    ShortEMA =  df.close.ewm(span=12, adjust=False).mean()
    # EMA 26 
    LongEMA = df.close.ewm(span=26, adjust=False).mean()
    # MACD Line
    MACD =  ShortEMA - LongEMA
    # signal Line
    signal = MACD.ewm(span=9, adjust=False).mean()
    return MACD,signal

def cal_EMA(df, span):
    """

    Args:
        df (dataframe): close price data
        span (int): num of day

    Returns:
        dataframe : EMA(num of day) close price data

    """

    return df.close.ewm(span=span, adjust=False).mean()

def get_close_history(client, config)-> pd.DataFrame:
    """

    Args:
        config (dictionary): should have symbol, interval, starttime
        client (binance.client): client of binance

    Returns:
        dataframe : all close price data
        
    """

    bars = client.get_historical_klines(config["symbol"], config["interval"], config["starttime"])
    bars = [line[4] for line in bars]
    return pd.DataFrame(bars, columns=['close'])

def read_config(path_json):
    """

    Args:
        path_json (string): path json file

    Returns:
        dictionary: data of json file

    """
    with open(path_json) as js:
        return json.load(js)