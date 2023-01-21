import pandas as pd
from yfinance import download
from datetime import datetime, timedelta
from cryptography.fernet import Fernet
from pickle import load
import os
from random import random
from time import gmtime, mktime
from ta.trend import *
from ta.momentum import *
from ta.volatility import *

class Strategy:
	def __init__(self, exchange):
		self.df = -1
		self.data = -1
		self.exchange = exchange+"-EUR"
		self.interval = "1h" # hours
		self.invest = 0.99

		print("b6")
		self.loadModel()
		print("b7")

		self.attributes = ["MACD","macV","rsV","signal","ATR","pband","wband","donpband","donwband","kama","ADX",
						"2RSI","4ema_diff","5ema_diff","2macV","4macV","5macV","2rsV","4rsV","5rsV","roc"]

		# parametri
		# self.tassa = 0.01
		# self.moltiplicatore = 1

	def loadModel(self):
		print("Starting to load model...")
		#from sktime.classification.kernel_based import RocketClassifier
		fernet = Fernet(os.environ['FERNET'])
		f = open("cmodel.pkl","rb")
		text = f.read()
		f.close()
		f = open("model.pkl","wb")
		f.write(fernet.decrypt(text))
		f.close()
		with open("model.pkl","rb") as model:
			self.model = load(model)
		print("Finished loading model.")

	def check_basic_signal(self):
		outside = abs(self.df.pband.iloc[-1])>1.1 or abs(self.df.pband.iloc[-1])<-0.1
		return outside

	def checkEnter(self, must_be_new=True):
		self.updateData(must_be_new=must_be_new)
		strategy = "-"
		trailing_delta = 0.01

		# Pre check
		
		if not(self.check_basic_signal()):
			return strategy, trailing_delta

		prediction = int(self.model.predict(self.df[attributes].iloc[-1].values.reshape(1,1,len(attributes))))
		if prediction == 1:
			strategy = "long5min"
		elif prediction == 2:
			strategy = "short5min"
		return strategy, trailing_delta

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
		return False

	def getRawData(self,must_be_new=True): # CONTROLLARE CHE SIA AGGIORNATO
		STEP = 400

		i = 0
		while i<10:
			self.df = download(self.exchange, start=(datetime.now()-timedelta(hours=STEP)).date(), end=datetime.now(), interval=self.interval, auto_adjust=False, prepost=False).astype(float).sort_index()
			if not must_be_new:
				break
			struct_time = gmtime(self.df.index[-1].timestamp())
			seconds = mktime(struct_time)
			if (datetime.utcnow().timestamp()-seconds)/60<20:
				break
			i += 1
			sleep(10)
		if i==10:
			raise Exception("Couldn't fetch data correctly.")
		self.df.index.names = ["Gmt time"]
		self.df = self.df[['Open','High','Low','Close','Volume']]
		self.data = self.df

	def updateData(self,must_be_new=True):
		self.getRawData(must_be_new)
		# Analyzing data

		# Normalizing parameters
		RSI = 100
		_MACD = 766.6113797470252
		MACV = 415.2976664892511
		RSV = 21.52645746367356
		SIGNAL = 1843.5330524851227
		EMA_DIFF = 106.97171332824632
		ATR = 0.05599500445196899
		# _2EMA_DIFF = 136.0111815154935
		# _3EMA_DIFF = 203.47311880316192
		_4EMA_DIFF = 5310.768473088647
		_5EMA_DIFF = 7746.271519356338
		KAMA = 58875.295759260654
		_2MACV = 266.49301358193435
		_4MACV = 199.67379715028846
		_5MACV = 176.26863911375267
		_2RSV = 14.564202956429801
		_4RSV = 9.77232108928448
		_5RSV = 8.691409908219972
		ROC = 49.49301526912332
		
		rsi = RSIIndicator(self.df['Close'])
		self.df["RSI"] = rsi.rsi()/RSI
		rsi = RSIIndicator(self.df['Close'],5)
		self.df["2RSI"] = rsi.rsi()/RSI
		rsi = RSIIndicator(self.df['Close'],20)
		self.df["3RSI"] = rsi.rsi()/RSI
		rsi = RSIIndicator(self.df['Close'],30)
		self.df["4RSI"] = rsi.rsi()/RSI

		macd = MACD(self.df['Close'])
		self.df['MACD'] = macd.macd_diff()/_MACD
		self.df['signal'] = macd.macd_signal()/MACV

		self.df['macV'] = (self.df['MACD']-self.df['MACD'].shift(1))/(2*MACV)
		self.df['rsV'] = (self.df['RSI']-self.df['RSI'].shift(1))/(2*RSV)
		self.df['macV'] = (self.df['MACD']-self.df['MACD'].shift(1))/(2*MACV)
		self.df['2macV'] = (self.df['MACD']-self.df['MACD'].shift(2))/(3*_2MACV)
		# self.df['3macV'] = (self.df['MACD']-self.df['MACD'].shift(3))/(4*_3MACV)
		self.df['4macV'] = (self.df['MACD']-self.df['MACD'].shift(4))/(5*_4MACV)
		self.df['5macV'] = (self.df['MACD']-self.df['MACD'].shift(5))/(6*_5MACV)
		self.df['rsV'] = (self.df['RSI']-self.df['RSI'].shift(1))/(2*RSV)
		self.df['2rsV'] = (self.df['RSI']-self.df['RSI'].shift(2))/(3*_2RSV)
		# self.df['3rsV'] = (self.df['RSI']-self.df['RSI'].shift(3))/(4*_3RSV)
		self.df['4rsV'] = (self.df['RSI']-self.df['RSI'].shift(4))/(5*_4RSV)
		self.df['5rsV'] = (self.df['RSI']-self.df['RSI'].shift(5))/(6*_5RSV)

		self.df['EMA12'] = ema_indicator(self.df['Close'], 12)
		self.df['EMA26'] = ema_indicator(self.df['Close'], 26)
		self.df['EMA32'] = ema_indicator(self.df['Close'], 32)
		self.df['EMA50'] = ema_indicator(self.df['Close'], 50)
		self.df['EMA100'] = ema_indicator(self.df['Close'], 100)
		self.df['EMA200'] = ema_indicator(self.df['Close'], 200)
		self.df['ema_diff'] = (self.df['EMA12']-self.df['EMA26'])/EMA_DIFF
		# self.df['2ema_diff'] = (self.df['EMA12']-self.df['EMA32'])/_2EMA_DIFF
		# self.df['3ema_diff'] = (self.df['EMA12']-self.df['EMA50'])/_3EMA_DIFF
		self.df['4ema_diff'] = (self.df['EMA12']-self.df['EMA100'])/_4EMA_DIFF
		self.df['5ema_diff'] = (self.df['EMA12']-self.df['EMA200'])/_5EMA_DIFF

		atr = AverageTrueRange(self.df['High'],self.df['Low'],self.df['Close'])
		self.df['ATR'] = atr.average_true_range()/self.df['Close']/ATR

		bollinger = BollingerBands(self.df['Close'])
		self.df['pband'] = bollinger.bollinger_pband()
		self.df['wband'] = bollinger.bollinger_wband()

		donchian = DonchianChannel(self.df['High'],self.df['Low'],self.df['Close'])
		self.df['donpband'] = donchian.donchian_channel_pband()
		self.df['donwband'] = donchian.donchian_channel_wband()

		kama = KAMAIndicator(self.df['Close'])
		self.df['kama'] = kama.kama()/KAMA

		roc = ROCIndicator(self.df['Close'])
		self.df['roc'] = roc.roc()/ROC

		adx = ADXIndicator(self.df['High'],self.df['Low'],self.df['Close'])
		self.df['ADX'] = adx.adx()/100

		self.df = self.df[self.attributes]

	def get_current_state(self):
		self.updateData(must_be_new=False)
		prediction = int(self.model.predict(self.df[self.attributes].iloc[-1].values.reshape(1,1,len(self.attributes))))
		r = f"pband: {self.df.pband.iloc[-1]} | isOutside (0,1): {self.check_basic_signal()} | prediction: {prediction}"
		return r

