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