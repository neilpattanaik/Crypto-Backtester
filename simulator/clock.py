import datetime
import pandas as pd

class Clock:
    def __init__(self, trading_universe, granularity, data_provider, trading_start_timestamp, trading_end_timestamp):
        self.trading_universe = trading_universe
        self.granularity = granularity
        self.data_provider = data_provider
        self.current_timestamp = trading_start_timestamp
        self.finishtrading = trading_end_timestamp

    def get_historical_candles(self, coins, start_timestamp, end_timestamp):
        data = {}
        for coin in coins:
            data[coin] = self.data_provider.get_data(coin, start_timestamp, end_timestamp, self.granularity)
        return pd.concat(data, axis=1)

    def tick(self, portfolio_state):
        if self.current_timestamp is None:
            raise ValueError("Clock has not been initialized with a current timestamp.")
        
        if self.finishtrading <= self.current_timestamp + self.granularity.timedelta:
            print("Finished!")
            raise Exception
        
        if portfolio_state.current_timestamp is None:
            portfolio_state.current_timestamp = self.current_timestamp
        
        portfolio_state.current_timestamp += self.granularity.timedelta
        self.current_timestamp = portfolio_state.current_timestamp
        return portfolio_state

    def get_candles(self, coins=None):
        if coins is None:
            coins = self.trading_universe
        end_timestamp = self.current_timestamp
        start_timestamp = end_timestamp - self.granularity.timedelta
        return self.get_historical_candles(coins, start_timestamp, end_timestamp)

    def get_previous_timestamps(self, n):
        timestamps = [self.current_timestamp - i * self.granularity.timedelta for i in range(1, n + 1)]
        return timestamps
