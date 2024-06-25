import datetime
from simulator.clock import Clock
from simulator.trade import Trade
from simulator.broker import Broker
from simulator.trader import Trader
from simulator.portfoliostate import PortfolioState
from simulator.pairs_trading_strategy import PairsTradingStrategy
from simulator.interval import interval
from simulator.coin import coin
from simulator.dataprovider import DataProvider

# Set Params
data_start_timestamp = datetime.datetime.now() - datetime.timedelta(days=60)
end_timestamp = datetime.datetime.now()
trading_start_timestamp = datetime.datetime.now() - datetime.timedelta(days=30)
starting_cash = 10000
granularity = interval('1h')
trading_universe = [coin('ETHUSDT', ''), coin('BTCUSDT', '')]
strategy = PairsTradingStrategy(lookback=20, z_threshold=2.0)


# Initialize components
data_provider = DataProvider(trading_universe, data_start_timestamp, end_timestamp, granularity)
clock = Clock(trading_universe, granularity, data_provider, trading_start_timestamp, end_timestamp)
portfolio = PortfolioState(starting_cash, trading_universe)
trader = Trader(strategy)
broker = Broker()

while True:
    current_candles = clock.get_candles()
    lookback_stamps = clock.get_previous_timestamps(trader.strategy.lookback)
    lookback_candles = clock.get_historical_candles(trading_universe, lookback_stamps[-1], lookback_stamps[0])
    trades = trader.decide_trades(portfolio, current_candles, lookback_stamps)
    portfolio = broker.execute(portfolio, trades)
    
    portfolio = clock.tick(portfolio)
    portfolio.brokered = False  # Reset brokered status after each tick
    print(portfolio)
