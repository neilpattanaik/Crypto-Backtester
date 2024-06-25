import pandas as pd
from simulator.candleFactory import candleFactory
from simulator.coin import coin
from simulator.interval import interval

class DataProvider:
    def __init__(self, trading_universe, start, end, granularity):
        self.candle_factory = candleFactory(trading_universe, start, end, granularity)

    def get_data(self, coin):
        return self.candle_factory.downloadTokenCandles(coin)
    
    def get_all_data(self):
        return self.candle_factory.downloadAllCandles()
