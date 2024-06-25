import pandas as pd
from simulator.trade import Trade

class strategy:
    def __init__(self, *args):
        # Class must have self.lookback, param determines # of timestamps to provide with trading data in prev_candles. excludes current.
        self.lookback = 0 


    def generate_trades(self, portfolio_state, current_candles, lookback_candles):
        trades = []
        ###Some trade generation logic

        return trades
