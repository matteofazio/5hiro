import pandas as pd
import pandas_ta as pa
from yfinance import download
from datetime import datetime, timedelta
from xgboost import XGBClassifier
from cryptography.fernet import Fernet
import os
from random import random

class Strategy:
	def __init__(self, exchange):
		self.df = -1
		self.exchange = exchange+"-EUR"
		self.interval = 5 # minutes
		self.invest = 0.99

		self.loadModel()

		# parametri
		# self.tassa = 0.01
		# self.moltiplicatore = 1

	def loadModel(self):
		fernet = Fernet(os.environ['FERNET'])
		f = open("cmodel.json","rb")
		text = f.read()
		f.close()
		f = open("model.json","wb")
		f.write(fernet.decrypt(text))
		f.close()
		self.model = XGBClassifier()
		self.model.load_model("model.json")


	def checkEnter(self):
		self.updateData()
		prediction = int(self.model.predict(self.df.iloc[-1:]))
		if prediction == 1:
			strategy = "long5min"
		elif random()<0.1:
			strategy = "random"
		sl = 0
		tp = 0
		return strategy, sl, tp

	def actOnOpenPosition(self):
		return [False,""] # trail stop to be implemented

	def check_exit(self):
		# this is actually something not necessary, since
		# stopCalls will be automated. But is good to have
		# to both add security, and also for a possible
		# future generalization
		"""if self.strategy != "-":
			if "short" in self.strategy:
				if self.stopCallShort():
					self.strategy = "-"
			elif "short" not in self.strategy:
				if self.stopCallLong():
					self.strategy = "-"
		return self.strategy == "-"
		"""
		return

	def getRawData(self): # CONTROLLARE CHE SIA AGGIORNATO
		STEP = 50
		interval = "5m"

		self.df = download(self.exchange, start=(datetime.now()-timedelta(minutes=STEP)).date(), end=datetime.now(), interval=interval, auto_adjust=False, prepost=False)
		self.df.index.names = ["Gmt time"]
		self.df = self.df[['Open','High','Low','Close','Volume']]

	def updateData(self):
		self.getRawData()
		# Analyzing data
		self.df["RSI"] = pa.rsi(self.df.Close, length=16)
		self.df["CCI"] = pa.cci(self.df.High, self.df.Low, self.df.Close, length=16)
		self.df["AO"] = pa.ao(self.df.High, self.df.Low)
		self.df["MOM"] = pa.mom(self.df.Close, length=16)
		a = pa.macd(self.df.Close)
		self.df = self.df.join(a)
		self.df["ATR"] = pa.atr(self.df.High, self.df.Low, self.df.Close, length=16)
		self.df["BOP"] = pa.bop(self.df.Open, self.df.High, self.df.Low, self.df.Close, length=16)
		self.df["RVI"] = pa.rvi(self.df.Close)
		a = pa.dm(self.df.High, self.df.Low, length=16)
		self.df = self.df.join(a)
		a = pa.stoch(self.df.High, self.df.Low, self.df.Close)
		self.df = self.df.join(a)
		a = pa.stochrsi(self.df.Close, length=16)
		self.df = self.df.join(a)
		self.df["WPR"] = pa.willr(self.df.High, self.df.Low, self.df.Close, length=16)
		attributes = ['RSI', 'CCI', 'AO', 'MOM', 'MACD_12_26_9', 'MACDh_12_26_9', 'MACDs_12_26_9', 'ATR','BOP', 'RVI', 'DMP_16', 'DMN_16', 'STOCHk_14_3_3', 'STOCHd_14_3_3','STOCHRSIk_16_14_3_3', 'STOCHRSId_16_14_3_3', 'WPR']
		self.df = self.df[attributes]

	def get_current_state(self):
		"""r = f"Close: {self.df.iloc[-1]['Close']} | "
		r += f"macd_diff: {self.df.iloc[-1]['macd_diff']} | "
		r += f"rocEMA100: {self.df.iloc[-1]['rocEMA100']} | "
		r += f"bollinger_pband: {self.df.iloc[-1]['bollinger_pband']} | "
		r += f"bollinger_wband: {self.df.iloc[-1]['bollinger_wband']}"
		return r
		"""
		return


	def getData(asset):
		SPAN = 500 # < 720
		i = 0
		while i<10:
			data = download(f"{asset}-EUR", start=datetime.now()-timedelta(hours=500), end=datetime.now(), interval="1h", auto_adjust=False, prepost=False).astype(float).sort_index()
			if data.iloc[-1]['Open'] == data.iloc[-1]['Close']:
				break
			i += 1
			sleep(10)
		return data.iloc[:-1]