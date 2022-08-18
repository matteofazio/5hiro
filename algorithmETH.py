from numpy import linspace, meshgrid, array, arctan
from ta.trend import *
from ta.momentum import *
from ta.volatility import *
import pandas as pd

class AlgorithmETH:
	def __init__(self, tassa, moltiplicatore):
		self.df = -1

		# parametri
		self.tassa = tassa
		self.moltiplicatore = moltiplicatore

		# stop calls
		self.stopWinMACD = self.tassa+0.4/self.moltiplicatore
		self.stopLossMACD = (0.01)/self.moltiplicatore
		self.stopWinBollinger = self.tassa+0.4/self.moltiplicatore
		self.stopLossBollinger = (0.03)/self.moltiplicatore
		self.lifespan = 0

		# parametri periodi
		self.ADXperiodo = 14
		self.periodiB = 6
		self.periodiL = 66
		self.Inclinazione = 23
		self.Periodo = 25
		self.longPeriod = 3*self.Periodo

		self.Breve = self.periodiB
		self.Lunga = self.periodiL

		self.strategia = "-"


	# ========================= funzioni dell'algoritmo ========================= #
	def buy(self, t):
		macd = self.df[f'EMA{self.Breve}'][t]>self.df[f'EMA{self.Lunga}'][t]
		inclinazioneMACD = 15<self.df[f'inclinazione_perc{self.Periodo}'][t]<60 and 10<self.df[f'inclinazione_perc{self.longPeriod}'][t]<45
		
		sar = self.df['psar_di'][t]==False
		aroon = self.df['aroon_indicator'][t]>-70
		inclinazioneBollinger = -15<self.df[f'inclinazione_perc{self.Periodo}'][t]
		bollinger = self.df['bollinger_pband'][t]<0.2
		if bollinger: self.lifespan = 8
		self.lifespan -= 1
		
		if macd and inclinazioneMACD and False:
			adx = self.df['adx'][t]>35
			if sar and adx:
				self.strategia = "MACD"
		elif inclinazioneBollinger and sar and aroon:
			adx = self.df['adx'][t]>20
			if self.lifespan>0 and adx:
				self.strategia = "BOLLINGER"
			self.lifespan = 0
		return self.strategia != "-"

	def sell(self, t, entrata):
		if self.strategia == "MACD":
			if self.df[f'EMA{self.Breve}'][t]<self.df[f'EMA{self.Lunga}'][t] or self.stopCallMacd(t,entrata):
				self.strategia = "-"
		elif self.strategia == "BOLLINGER":
			if self.stopCallBollinger(t,entrata):
				self.strategia = "-"
		return self.strategia == "-"

	def stopCallMacd(self, t, entrata):
		sar = self.moltiplicatore*(self.df['Close'][t]*(1-self.tassa)-entrata)/entrata>=0 and self.df['psar_di'][t]==True
		upper = self.df['Close'][t]>entrata*(1+self.stopWinMACD)#*(1+self.df['atr_perc'][t]))
		lower = self.df['Close'][t]<entrata*(1-self.stopLossMACD)#*(1+self.df['atr_perc'][t]))
		return upper or lower or sar

	def stopCallBollinger(self, t, entrata):
		sar = self.moltiplicatore*(self.df['Close'][t]*(1-self.tassa)-entrata)/entrata>=0 and self.df['psar_di'][t]==True
		upper = self.df['Close'][t]>entrata*(1+self.stopWinBollinger)#*(1+self.df['atr_perc'][t]))
		lower = self.df['Close'][t]<entrata*(1-self.stopLossBollinger)#*(1+self.df['atr_perc'][t]))
		return upper or lower or sar

	def analyzeDf(self):
		# EMA
		self.df[f'EMA{self.periodiB}'] = ema_indicator(self.df['Close'], self.periodiB, False)
		self.df[f'EMA{self.periodiL}'] = ema_indicator(self.df['Close'], self.periodiL, False)
		macd = MACD(self.df['Close'])
		self.df['macd'] = macd.macd()
		self.df['signal'] = macd.macd_signal()

		# ADX
		adxI = ADXIndicator(self.df['High'],self.df['Low'],self.df['Close'], self.ADXperiodo, False)
		self.df['pos_directional_indicator'] = adxI.adx_pos()
		self.df['neg_directional_indicator'] = adxI.adx_neg()
		self.df['adx'] = adxI.adx()

		# RSI
		rsiI = RSIIndicator(self.df['Close'])
		self.df['rsi'] = rsiI.rsi()

		# ATR
		atr = AverageTrueRange(self.df['High'],self.df['Low'],self.df['Close'])
		self.df['atr'] = atr.average_true_range()
		self.df['atr_perc'] = self.df['atr']/self.df['Close']

		# Bollinger Bands
		bollinger = BollingerBands(self.df['Close'],200)
		self.df['bollinger_hband'] = bollinger.bollinger_hband()
		self.df['bollinger_lband'] = bollinger.bollinger_lband()
		self.df['bollinger_wband'] = bollinger.bollinger_wband()
		self.df['bollinger_hband_indicator'] = bollinger.bollinger_hband_indicator()
		self.df['bollinger_pband'] = bollinger.bollinger_pband()

		# inclinazione_perc
		zoom = 2000
		self.df[f'inclinazione_perc{self.Periodo}'] = zoom*200*arctan(  (self.df[f'EMA{self.periodiL}']-self.df[f'EMA{self.periodiL}'].shift(self.Periodo))/(self.Periodo*self.df[f'EMA{self.periodiL}'].shift(self.Periodo))  )/(3.14)
		self.df[f'inclinazione_perc{self.longPeriod}'] = zoom*200*arctan(  (self.df[f'EMA{self.periodiL}']-self.df[f'EMA{self.periodiL}'].shift(self.longPeriod))/(self.longPeriod*self.df[f'EMA{self.periodiL}'].shift(self.longPeriod))  )/(3.14)

		# Parabolic SAR
		parabolicSar = PSARIndicator(self.df['High'],self.df['Low'],self.df['Close'])
		self.df['psar'] = parabolicSar.psar()
		self.df['psar_di'] = self.df['psar']>self.df['Close']
		self.df['psar_down_indicator'] = parabolicSar.psar_down_indicator()

		# Aroon
		aroon = AroonIndicator(self.df['Close'])
		self.df['aroon_indicator'] = aroon.aroon_indicator()
