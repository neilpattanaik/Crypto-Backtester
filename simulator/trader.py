class Trader:
    def __init__(self, strategy):
        self.strategy = strategy

    def decide_trades(self, portfolio_state, current_candles, lookback_candles):
        return self.strategy.generate_trades(portfolio_state, current_candles, lookback_candles)
