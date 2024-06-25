class Trade:
    def __init__(self, trade_type, token, qty_traded, execution_price):
        if trade_type not in ["long", "short"]:
            raise ValueError("trade_type must be 'long' or 'short'")
        self.trade_type = trade_type
        self.token = token
        self.qty_traded = qty_traded
        self.execution_price = execution_price
