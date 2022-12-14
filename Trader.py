import requests
from time import sleep, time
from binance.spot import Spot
import os

class Trader:
	def __init__(self,exchange):
		self.exchange = exchange

		# dati api
		self.api_key = os.environ['API_KEY']
		self.api_sec = os.environ['API_SEC']
		self.client = Spot(key=self.api_key, secret=self.api_sec)

		# portfolio statistics
		self.staticMoney = 10
		self.staticETH = 0.0003
		self.money = 0
		self.stocks = 0
		self.euro = 0
		self.get_balance()

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
			if i["asset"] == "ETH":
				stocks = float(i["free"])-self.staticETH
			if i["asset"] == "BUSD":
				money = float(i["free"])-self.staticMoney
			if i["asset"] == "EUR":
				self.euro = float(i["free"])
		self.money = money
		self.stocks = stocks
		return money,stocks

	def get_trade_history(self, ora):
		"""params = {
			'symbol': 'ETHEUR',
			'recvWindow': 60000
		}
		v = self.client.my_trades(**params)
		df = pd.DataFrame(v)
		if not df.empty:
			df = df.loc[df["time"]>ora].set_index("time").sort_index(ascending=False)
			costo = df["quoteQty"].astype(float).sum()
			tassa = df["commission"].astype(float).sum()
			volume = df["qty"].astype(float).sum()
			price = df["price"].astype(float).mean()
			return True,costo,tassa,price,volume
		else:
			return False,0,0,0,0"""

	def get_volume(self,ora):
		#flag,costo,tassa,price,volume = self.get_trade_history(ora)
		#return volume
		return 0

	def openOrder(self):
		return
		"""print(f"{self.currentNameResult}EUR")
		self.get_balance()

		if self.shorting==True or "short" in self.A.strategia:
			params = {
				'symbol': 'ETHBUSD',
				'side': 'SELL',
				'type': 'MARKET',
				'quantity': round(self.stocks,5), # <- sus, devo mettere i money in ETH?
				'recvWindow': 60000
			}
		else:
			params = {
				'symbol': 'ETHBUSD',
				'side': 'BUY',
				'type': 'MARKET',
				'quoteOrderQty': round(self.money,2),
				'recvWindow': 60000
			}

		v = self.client.new_order(**params)
		# add stopcalls
		return v"""

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