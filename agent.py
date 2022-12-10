from numpy import arctan
from ta.trend import *
from ta.momentum import *
from ta.volatility import *
from algorithmETH import AlgorithmETH
from time import time
import requests
import urllib.parse
import hashlib
import hmac
import base64
from json import dumps,loads
from time import sleep, time
import pandas as pd
from binance.spot import Spot
import os

class AGENT:
	def __init__(self):
		# dati api
		self.api_key = os.environ['API_KEY']
		self.api_sec = os.environ['API_SEC']
		self.client = Spot(key=self.api_key, secret=self.api_sec)

		# parametri
		self.tassa = 0.002
		self.moltiplicatore = 1
		self.invest = 1 # 100%

		# algoritmi
		self.ETH = AlgorithmETH(self.tassa,self.moltiplicatore)
		self.A = self.ETH

		# Parametri della simulazione
		self.staticMoney = 10
		self.staticETH = 0.0003

		self.strategia = "-"
		self.currentName = "ETH"

		self.money = 0
		self.stocks = 0
		self.euro = 0
		self.get_balance()
		self.dentro = False
		self.entrata = 0
		self.ora = 0
		self.shorting = False

	# ========================= funzioni di gestione ========================= #
	def buy(self, now, data, forced=False, short=False):
		self.A.df = data.astype(float)
		self.A.analyzeDf()
		if not self.dentro and self.A.check_enter(-1) == True:
			self.ora = int((time()-60)*1000)
			self.get_balance()
			spesa = self.invest*self.money

			if "short" in self.A.strategia and False: # <- to activate
				self.shorting = True
			output = self.enter_order()

			k = 0
			while k<8:
				sleep(10)
				flag,costo,tassa,price,volume = self.get_trade_history(self.ora)
				if flag:
					self.entrata = price
					break
				k += 1

			if costo!=0 or True:
				self.dentro = True
			self.get_balance()
			return [True,f"Enter: {self.get_price()} [{self.A.strategia}]"]
			return [True,f"[{self.A.strategia}] Enter: Crypto:{self.stocks} {self.currentName}({costo}*{self.moltiplicatore}={costo*self.moltiplicatore}$) / Balance:{self.money}$ || {output}"]

		elif forced:
			self.get_balance()
			spesa = self.invest*self.money
			if short==True:
				self.shorting = True
			output = self.enter_order()

			print(output)
			k = 0
			while k<8:
				sleep(10)
				flag,costo,tassa,price,volume = self.get_trade_history(self.ora)
				print(flag,costo,tassa,price)
				if flag:
					self.entrata = price
					break
				k += 1
			if costo!=0:
				self.dentro = True
			self.get_balance()
			return [True,f"[{self.A.strategia}] Enter: Crypto:{self.stocks} {self.currentName}({costo}*{self.moltiplicatore}={costo*self.moltiplicatore}$) / Balance:{self.money}$ || {output}"]
		return [False,""]

	def sell(self, now, data, forced=False):
		self.A.df = data.astype(float)
		self.A.analyzeDf()
		if (self.dentro and self.A.check_exit(-1, self.entrata) == True) or forced:
			self.dentro = False
			#output = self.exit_order() # <- to activate
			if (self.shorting==True or "short" in self.strategia):
				self.shorting = False
			
			sleep(10)
			self.get_balance()

			m = self.current
			self.current = -1
			return [True,f"Exit: {self.get_price()}"]
			return [True,f"Exit: Crypto:{self.stocks} {self.currentName} / Balance:{round(self.money,2)}$ || {output}"]
		return [False,""]

	def get_total_balance(self):
		self.get_balance()
		return f"Balance: {self.money}$+({self.staticMoney}$) / Crypto: {self.stocks}{self.currentName}({self.get_price()*self.stocks}$)({self.get_price()}ETH/$) / Total(ETH+BUSD): {self.money+self.get_price()*self.stocks}$ /Homecash: {self.euro}€"


	def get_current_state(self, data):
		self.A.df = data.astype(float)
		self.A.analyzeDf()
		return self.A.get_current_state()


	# ========================= funzioni di richiesta ========================= #	
	def get_price(self):
		return float(requests.get(f'https://api.binance.com/api/v3/ticker/price?symbol={self.currentName}EUR').json()["price"])

	def get_balance(self):
		params = {
			'recvWindow': 60000
		}
		v = self.client.account(**params)["balances"]
		money = 0
		stocks= 0
		for i in v:
			if i["asset"] == "ETH":
				stocks = float(i["free"])-self.staticETH
			if i["asset"] == "BUSD":
				money = float(i["free"])-self.staticMoney
			if i["asset"] == self.currentName:
				self.euro = float(i["free"])
		self.money = money
		self.stocks = stocks
		return money,stocks

	def get_trade_history(self, ora):
		params = {
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
			return False,0,0,0,0

	def get_volume(self):
		flag,costo,tassa,price,volume = self.get_trade_history(self.ora)
		return volume

	def enter_order(self):
		return
		print(f"{self.currentNameResult}EUR")
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
		return v

	def exit_order(self):
		return
		print(f"{self.currentNameResult}EUR")
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
