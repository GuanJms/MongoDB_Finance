from alpaca.trading.client import TradingClient, OrderRequest

API_NAME = 'PK4KNHN1288FU75AUBDI'
API_KEY = '2pfsnioo6cjRVs4PqVlPHKd2WRl47yndffIVqQpj'

trading_client = TradingClient(API_NAME, API_KEY)

account = trading_client.get_account()

stock = 'NIO'
order_request = OrderRequest(symbol=stock, qty= 1, side="buy", type="market", time_in_force="day")
trading_client.submit_order(order_request)

order_request = OrderRequest(symbol=stock, qty= 1, side="sell", type="market", time_in_force="day")
trading_client.submit_order(order_request)