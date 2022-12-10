from numpy import linspace, meshgrid, array, arctan
from ta.trend import *
from ta.momentum import *
from ta.volatility import *
from cryptography.fernet import Fernet
import pandas as pd
import os

f = open("ai.md","rb")
w = open("ai.py","w")
key = os.environ['FERNET']
fernet = Fernet(key)
text = fernet.decrypt(f.read()).decode("utf-8")
w.write(text)
w.close()
f.close()

from ai import AI

class AlgorithmETH:
	def __init__(self, tassa, moltiplicatore):
		self.df = -1
		self.ai = AI()

		# parametri
		self.tassa = tassa
		self.moltiplicatore = moltiplicatore

		# stop calls
		self.stopWin = 0
		self.stopLoss = 0

		self.strategia = "-"


	# ========================= funzioni dell'algoritmo ========================= #
	def check_enter(self, t):
		self.strategia,calls = self.ai.eval(self.df,t)
		if self.strategia != "-":
			self.stopWin = calls[0]
			self.stopLoss = calls[1]
		return self.strategia != "-"

	def check_exit(self, t, entrata):
		# this is actually something not necessary, since
		# stopCalls will be automated. But is good to have
		# to both add security, and also for a possible
		# future generalization
		if self.strategia != "-":
			if "short" in self.strategia:
				if self.stopCallShort():
					self.strategia = "-"
			elif "short" not in self.strategia:
				if self.stopCallLong():
					self.strategia = "-"
		return self.strategia == "-"

	def stopCallLong(self, t, entrata):
		upper = self.df['Close'][t]>entrata*(1+self.stopWin)
		lower = self.df['Close'][t]<entrata*(1-self.stopLoss)
		return upper or lower

	def stopCallLong(self, t, entrata):
		upper = self.df['Close'][t]<entrata*(1-self.stopWin)
		lower = self.df['Close'][t]>entrata*(1+self.stopLoss)
		return upper or lower

	def analyzeDf(self):
		# EMA
		self.df[f'EMA{100}'] = ema_indicator(self.df['Close'],100,False)
		rocEMA100 = ROCIndicator(self.df['EMA100'])
		self.df['rocEMA100'] = rocEMA100.roc() #
		
		self.df['distance'] = (self.df['Close']-self.df['EMA100'])/self.df['EMA100'] #
		macd = MACD(self.df['Close'])
		self.df['macd_diff'] = macd.macd_diff() #

		# roc
		rocBreve = ROCIndicator(self.df['Close'])
		self.df['rocM'] = rocBreve.roc()
		rocBreve = ROCIndicator(self.df['Close'],5)
		self.df['roc5'] = rocBreve.roc()

		# Bollinger Bands
		bollinger = BollingerBands(self.df['Close'],100)
		self.df['bollinger_wband'] = bollinger.bollinger_wband() #
		self.df['bollinger_pband'] = bollinger.bollinger_pband() #

	def get_current_state(self):
		r = f"Close: {self.df.iloc[-1]['Close']} | "
		r += f"macd_diff: {self.df.iloc[-1]['macd_diff']} | "
		r += f"rocEMA100: {self.df.iloc[-1]['rocEMA100']} | "
		r += f"bollinger_pband: {self.df.iloc[-1]['bollinger_pband']} | "
		r += f"bollinger_wband: {self.df.iloc[-1]['bollinger_wband']}"
		return r