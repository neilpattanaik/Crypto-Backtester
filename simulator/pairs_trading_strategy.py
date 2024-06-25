import pandas as pd
from simulator.trade import Trade

class PairsTradingStrategy:
    def __init__(self, lookback=20, z_threshold=2.0):
        self.lookback = lookback
        self.z_threshold = z_threshold

    def generate_trades(self, portfolio_state, current_candles):
        trades = []
        
        # Ensure we have data for at least two coins for pairs trading
        if len(portfolio_state.trading_universe) < 2:
            return trades

        # Get the two coins for pairs trading
        coin1, coin2 = portfolio_state.trading_universe[:2]

        if (coin1, 'close') not in current_candles.columns or (coin2, 'close') not in current_candles.columns:
            return trades
        
        # Calculate the price ratio
        price1 = current_candles[(coin1, 'close')]
        price2 = current_candles[(coin2, 'close')]
        ratios = price1 / price2

        # Calculate the rolling mean and rolling standard deviation
        ma1 = ratios.rolling(window=self.lookback).mean()
        ma2 = ratios.rolling(window=self.lookback*2).mean()
        std = ratios.rolling(window=self.lookback*2).std()
        zscore = (ma1 - ma2) / std

        # Generate trades based on z-score
        if zscore.iloc[-1] > self.z_threshold:
            # Price ratio is above the threshold, short coin1 and long coin2
            trades.append(Trade(trade_type="short", token=coin1, qty_traded=1, execution_price=price1.iloc[-1]))
            trades.append(Trade(trade_type="long", token=coin2, qty_traded=1, execution_price=price2.iloc[-1]))
        elif zscore.iloc[-1] < -self.z_threshold:
            # Price ratio is below the threshold, long coin1 and short coin2
            trades.append(Trade(trade_type="long", token=coin1, qty_traded=1, execution_price=price1.iloc[-1]))
            trades.append(Trade(trade_type="short", token=coin2, qty_traded=1, execution_price=price2.iloc[-1]))

        return trades
