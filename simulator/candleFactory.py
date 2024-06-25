import datetime
import os
import requests
import pandas as pd
from simulator.interval import interval
from simulator.coin import coin

class candleFactory:
    def __init__(self, tradingUniverse, start, end, granularity, forceDownload=False, cache_dir='cache'):
        self.tradingUniverse = tradingUniverse
        self.startUnixTime = interval.get_epoch_time(start) * 1000
        self.endUnixTime = interval.get_epoch_time(end) * 1000
        self.granularity = granularity
        self.forceDownload = forceDownload
        self.cache_dir = cache_dir
        self.endpoint = os.getenv("binance_endpoint", "https://api.binance.com/api/v3/klines?")

        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)

    def get_cache_filename(self, token_name):
        return os.path.join(self.cache_dir, f"{token_name}_{self.granularity.timeframe}.csv")

    def is_cache_valid(self, token_name):
        cache_file = self.get_cache_filename(token_name)
        if not os.path.exists(cache_file):
            return False

        df = pd.read_csv(cache_file, index_col=0, parse_dates=True)
        start_time = datetime.datetime.utcfromtimestamp(self.startUnixTime / 1000).replace(tzinfo=None)
        end_time = datetime.datetime.utcfromtimestamp(self.endUnixTime / 1000).replace(tzinfo=None)
        if df.index.min().to_pydatetime().replace(tzinfo=None) <= start_time and \
           df.index.max().to_pydatetime().replace(tzinfo=None) >= end_time:
            return True
        return False

    def clean_data(self, df):
        df = df[~df.index.duplicated(keep='first')]
        df.ffill(inplace=True)
        df = df.astype({
            "open": "float64",
            "high": "float64",
            "low": "float64",
            "close": "float64",
            "volume": "float64",
        })
        return df

    def downloadTokenCandles(self, token):
        paramstr = f"symbol={token.name}&interval={self.granularity.timeframe}"
        timestamps = [self.startUnixTime]
        currStamp = self.startUnixTime
        
        while currStamp < self.endUnixTime:
            if (self.endUnixTime - currStamp) / self.granularity.timedelta.total_seconds() > 999:
                currStamp += int(self.granularity.timedelta.total_seconds() * 999 * 1000)
                timestamps.append(currStamp)
            else:
                timestamps.append(self.endUnixTime)
                break

        open, high, low, close, volume, stamps = [], [], [], [], [], []
        
        for i in range(len(timestamps) - 1):
            startStamp = timestamps[i]
            endStamp = timestamps[i + 1]
            api_call_str = f"{self.endpoint}{paramstr}&startTime={startStamp}&endTime={endStamp}&limit=1000"
            response = requests.get(api_call_str)
            
            if response.status_code == 200:
                json_data = response.json()
                if json_data:
                    for item in json_data:
                        stamp = datetime.datetime.fromtimestamp(item[0] / 1000, datetime.timezone.utc).replace(tzinfo=None)
                        stamps.append(stamp)
                        open.append(float(item[1]))
                        high.append(float(item[2]))
                        low.append(float(item[3]))
                        close.append(float(item[4]))
                        volume.append(float(item[5]))
            else:
                raise Exception(f"Error fetching data. Got: {response.status_code} {response.text}")

        df = pd.DataFrame({
            "open": open,
            "high": high,
            "low": low,
            "close": close,
            "volume": volume,
        }, index=stamps)

        df = self.clean_data(df)
        return df

    def downloadAllCandles(self):
        frames = []
        for token in self.tradingUniverse:
            cache_file = self.get_cache_filename(token.name)

            if not self.forceDownload and self.is_cache_valid(token.name):
                df = pd.read_csv(cache_file, index_col=0, parse_dates=True)
                df = self.clean_data(df)
            else:
                df = self.downloadTokenCandles(token)
                df.to_csv(cache_file)

            df.columns = pd.MultiIndex.from_product([[token.name], df.columns])
            frames.append(df)

        result = pd.concat(frames, axis=1)
        return result
