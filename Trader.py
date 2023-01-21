import requests
from time import sleep, time
from binance.spot import Spot
import os

class Trader:
	def __init__(self,exchange):
		self.exchange = exchange
		self.LOT_STEP = 10**5 # for BTC, for ETH is 10**4

		# dati api
		self.api_key = os.environ['API_KEY']
		self.api_sec = os.environ['API_SEC']
		self.client = Spot(key=self.api_key, secret=self.api_sec)

		# portfolio statistics
		self.staticMoney = 50
		self.staticETH = 0.0000
		self.money = 0
		self.stocks = 0
		print("b4")
		self.get_balance()
		print("b5")

	def get_price(self):
		return float(requests.get(f'https://api.binance.com/api/v3/ticker/price?symbol={self.exchange}EUR').json()["price"])

	def get_balance(self):
		params = {
			'recvWindow': 60000
		}
		v = self.client.account(**params)["balances"]
		money = 0
		stocks= 0
		# da controllare
		for i in v:
			if i["asset"] == "BTC":
				stocks = float(i["free"])-self.staticETH
			if i["asset"] == "EUR":
				money = float(i["free"])-self.staticMoney
		self.money = money
		self.stocks = stocks
		return money,stocks
		
	def openOrder(self, short, trailing_delta):
		money,stocks = self.get_balance()
		price = get_price()
		quantity = floor((self.LOT_STEP)*money/price)/(self.LOT_STEP) # LOT_STEP is (0.0001 ETH) and (0.00001 BTC)
		if short==True:
			params_order = {
				'symbol': f'{self.exchange}EUR',
				'side': 'SELL',
				'type': 'MARKET',
				'quantity': quantity, # 0.0135 BTC
				'recvWindow': 60000
			}
			params_stop_trail = {
				'symbol': f'{self.exchange}EUR',
				'side': 'BUY',
				'type': 'STOP_LOSS_LIMIT',
				'quantity': quantity,
				'price': price,
				'timeInForce': 'GTC',
				'trailingDelta': 100,
				'recvWindow': 60000
			}
		else:
			params_order = {
				'symbol': f'{self.exchange}EUR',
				'side': 'BUY',
				'type': 'MARKET',
				'quantity': quantity,
				'recvWindow': 60000
			}
			params_stop_trail = {
				'symbol': f'{self.exchange}EUR',
				'side': 'SELL',
				'type': 'STOP_LOSS_LIMIT',
				'quantity': quantity,
				'price': price,
				'timeInForce': 'GTC',
				'trailingDelta': 100,
				'recvWindow': 60000
			}
		v = "-"
		v2 = "-"
		v3 = "-"
		try:
			print(1)
			v = self.client.new_order(**params_order)
			print(2)
			v2 = self.client.new_order(**params_stop_trail)
			print(3)
		except Exception as e:
			print(">",e)
			v3 = str(e)
		# add stopcalls
		return f"{v}\n{v2}\n{v3}"


	# ======== Useful non necessary requests ======== #
	def cancel_open_orders(self):
		params = {
			'symbol': 'BTCEUR',
			'recvWindow': 60000
		}
		v = self.client.cancel_open_orders(**params)
		# add stopcalls
		return v

	def get_current_open_orders(self):
		params = {
			'symbol': f'{self.exchange}EUR',
			'recvWindow': 60000
		}
		v = self.client.get_open_orders(**params)
		# add stopcalls
		return v

	def get_trade_history(self):
		params = {
			'symbol': f'{self.exchange}EUR',
			"startTime": int(time()*1000)-60*60*24*1000,
			"endTime": int(time()*1000)-5,
			'recvWindow': 60000
		}
		v = self.client.my_trades(**params)
		return str(v).replace("}, {","},\n{")

	def manual_buy_amount(self, eur):
		self.get_balance()
		params_order = {
			'symbol': f'{self.exchange}EUR',
			'side': 'BUY',
			'type': 'MARKET',
			'quoteOrderQty': eur,
			'recvWindow': 60000
		}
		v = self.client.new_order(**params_order)
		return v

	def manual_sell_amount(self, coin):
		self.get_balance()
		coin = floor((self.LOT_STEP)*coin)/(self.LOT_STEP)
		params_order = {
			'symbol': f'{self.exchange}EUR',
			'side': 'SELL',
			'type': 'MARKET',
			'quantity': coin,
			'recvWindow': 60000
		}
		v = self.client.new_order(**params_order)
		return v

	def closeOrder(self):
		return
		"""print(f"{self.currentNameResult}EUR")
		self.get_balance()
		if self.shorting==True or "short" in self.A.strategia:
			params = {
				'symbol': 'ETHBUSD',
				'side': 'BUY',
				'type': 'MARKET',
				'quoteOrderQty': round(self.money/2,2), # <- sus, devo mettere stocks in $?
				'recvWindow': 60000
			}
		else:
			params = {
				'symbol': 'ETHBUSD',
				'side': 'SELL',
				'type': 'MARKET',
				'quantity': round(self.stocks,5),#/2
				'recvWindow': 60000
			}
		v = self.client.new_order(**params)
		return v
		"""