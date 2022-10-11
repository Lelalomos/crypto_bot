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
        period9_high = df['high'].rolling(window=tenkansen_value).max()
        period9_low = df['low'].rolling(window=tenkansen_value).min()
        tenkan_sen = (period9_high + period9_low) / 2

        # Kijun-sen (Base Line): (26-period high + 26-period low)/2))
        period26_high = df['high'].rolling(window=kinjunsen_value).max()
        period26_low = df['low'].rolling(window=kinjunsen_value).min()
        kijun_sen = (period26_high + period26_low) / 2

        # Senkou Span A (Leading Span A): (Conversion Line + Base Line)/2))
        senkou_span_a = ((tenkan_sen + kijun_sen) / 2).shift(shift_value)

        # Senkou Span B (Leading Span B): (52-period high + 52-period low)/2))
        period52_high = df['high'].rolling(window=senkou_b_value).max()
        period52_low = df['low'].rolling(window=senkou_b_value).min()
        senkou_span_b = ((period52_high + period52_low) / 2).shift(shift_value)

        df['cloud_green_line_a'] = senkou_span_a
        df['cloud_red_line_b'] = senkou_span_b
        return df


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