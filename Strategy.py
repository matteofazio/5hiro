import pandas as pd
from yfinance import download
from datetime import datetime, timedelta
from time import time, sleep
from cryptography.fernet import Fernet
from pickle import load
import os
from random import random
from time import gmtime, mktime
from ta.trend import *
from ta.momentum import *
from ta.volatility import *
import requests
import talib
from scipy.signal import savgol_filter
from Strategies import *

class Strategy:
	def __init__(self, exchange):
		self.df = -1
		self.exchange = exchange
		self.interval = "1h" # hours
		self.invest = 0.99
		self.strategyManager = StrategyManager()

		self.attributes = ["angleFit","angleDerivative"]

	def checkEnter(self, must_be_new=True):
		self.updateData(must_be_new=must_be_new)
		return self.strategyManager.checkSignal(self.df)

	def getRawData(self,must_be_new=True): # CONTROLLARE CHE SIA AGGIORNATO
		STEP = 101

		i = 0
		while i<10:
			cols = ["Time","Open","High","Low","Close","Volume","Close_time","qtav","nTrades","taker_base_av","taker_quote_av","unused"]
			r = requests.get(f'https://api.binance.com/api/v3/klines?symbol={self.exchange}EUR&interval={self.interval}&limit={STEP}').json()
			self.df = pd.DataFrame(r,columns=cols).set_index("Time").apply(pd.to_numeric).sort_index()
			if not must_be_new:
				break
			seconds = self.df.index[-1]
			if (time()-seconds/1000)/60<2:
				break
			i += 1
			sleep(3)
		if i==10:
			raise Exception("Couldn't fetch data correctly.",seconds/1000,time(),(time()-seconds/1000)/60<2)
		self.df = self.df[['Open','High','Low','Close','Volume']].iloc[:-1]

	def updateData(self,must_be_new=True):
		self.getRawData(must_be_new)

		# Analyzing data
		# roc = ROCIndicator(self.df['Close'])
		# self.df['roc'] = roc.roc()

		# upperband, middleband, lowerband = talib.BBANDS(self.df['Close'], timeperiod=5, nbdevup=2, nbdevdn=2, matype=0)
		# self.df["bbup"] = upperband
		# self.df["bblow"] = lowerband
		# self.df["bbp"] = (self.df["Close"]-self.df["bblow"])/(self.df["bbup"]-self.df["bblow"])

		# dema = talib.DEMA(self.df["Close"], timeperiod=30)
		# self.df["dema"] = 100*(dema-self.df["Close"])/self.df["Close"]
		
		# candle = "CDLENGULFING"
		# self.df[candle] = getattr(talib, candle)(self.df['Open'], self.df['High'], self.df['Low'], self.df['Close'])

		angle = talib.LINEARREG_ANGLE(self.df["Close"], timeperiod=48)
		self.df["angle"] = angle
		self.df["angleFit"] = savgol_filter(self.df["angle"], 48, 3)
		self.df["angleDerivative"] = ((self.df["angleFit"].diff(periods=3))/3).fillna(0)
		self.df["angleDerivative"] = savgol_filter(self.df["angleDerivative"], 48, 3)

		self.df = self.df[self.attributes]

	def get_current_state(self):
		self.updateData(must_be_new=False)
		time = str(self.df.index[-1])
		angleFitValue = str(round(self.df["angleFit"].iloc[-1],2))
		angleDerivativeValue = str(round(self.df["angleDerivative"].iloc[-1],2))
		r = f"time: {time}, angleFit: {angleFitValue}, angleDerivative: {angleDerivativeValue}"
		return r

# decomment if needed
"""
def check_exit(self):
	# this is actually something not necessary, since
	# stopCalls will be automated. But is good to have
	# to both add security, and also for a possible
	# future generalization
	# if self.strategy != "-":
	# 	if "short" in self.strategy:
	# 		if self.stopCallShort():
	# 			self.strategy = "-"
	# 	elif "short" not in self.strategy:
	# 		if self.stopCallLong():
	# 			self.strategy = "-"
	# return self.strategy == "-"
	# return False
"""

# decomment if ai is used again
"""	def loadModel(self):
		return
		# print("Starting to load model...")
		#from sktime.classification.kernel_based import RocketClassifier
		# fernet = Fernet(os.environ['FERNET'])
		# f = open("cmodel.pkl","rb")
		# text = f.read()
		# f.close()
		# f = open("model.pkl","wb")
		# f.write(fernet.decrypt(text))
		# f.close()
		# with open("model.pkl","rb") as model:
		# 	self.model = load(model)
		# print("Finished loading model.")
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

adx = ADXIndicator(self.df['High'],self.df['Low'],self.df['Close'])
self.df['ADX'] = adx.adx()/100


in current state:
#prediction = int(self.model.predict(self.df[self.attributes].iloc[-1].values.reshape(1,1,len(self.attributes))))
in checkEnter
#prediction = int(self.model.predict(self.df[self.attributes].iloc[-1].values.reshape(1,1,len(self.attributes))))

"""