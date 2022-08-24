import pandas as pd
import json

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