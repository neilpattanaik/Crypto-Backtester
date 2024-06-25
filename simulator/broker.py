class Broker:
    def execute(self, portfolio, trades):
        if portfolio.brokered:
            raise ValueError("Cannot execute trades on an already brokered portfolio state.")
        for trade in trades:
            if trade.trade_type == "long":
                self._execute_long(portfolio, trade)
            elif trade.trade_type == "short":
                self._execute_short(portfolio, trade)
        portfolio.brokered = True
        return portfolio

    def _execute_long(self, portfolio, trade):
        cost = trade.qty_traded * trade.execution_price
        if portfolio.available_cash >= cost:
            portfolio.available_cash -= cost
            portfolio.open_long_positions[trade.token] = portfolio.open_long_positions.get(trade.token, 0) + trade.qty_traded
            portfolio.open_trades.append(trade)
        else:
            raise ValueError("Not enough cash to execute long trade.")

    def _execute_short(self, portfolio, trade):
        revenue = trade.qty_traded * trade.execution_price
        portfolio.available_cash += revenue
        portfolio.open_short_positions[trade.token] = portfolio.open_short_positions.get(trade.token, 0) + trade.qty_traded
        portfolio.open_trades.append(trade)
