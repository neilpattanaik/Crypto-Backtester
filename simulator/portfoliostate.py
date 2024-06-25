class PortfolioState:
    def __init__(self, starting_cash, trading_universe):
        self.starting_cash = starting_cash
        self.trading_universe = trading_universe
        self.available_cash = starting_cash
        self.open_long_positions = {}
        self.open_short_positions = {}
        self.open_trades = []
        self.closed_trades = []
        self.current_timestamp = None
        self.brokered = False

    def __repr__(self):
        return (f"PortfolioState(available_cash={self.available_cash}, open_long_positions={self.open_long_positions}, "
                f"open_short_positions={self.open_short_positions}, open_trades={len(self.open_trades)}, "
                f"closed_trades={len(self.closed_trades)}, current_timestamp={self.current_timestamp}, brokered={self.brokered})")
