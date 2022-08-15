from numpy import linspace, meshgrid, array, arctan
import matplotlib.pyplot as plt
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
		self.stopLossMACD = (0.03)/self.moltiplicatore
		self.stopWinBollinger = self.tassa+0.4/self.moltiplicatore
		self.stopLossBollinger = (0.07)/self.moltiplicatore

		# parametri periodi
		self.ADXperiodo = 14
		self.periodiB = 6
		self.periodiL = 66
		self.Inclinazione = 23
		self.Periodo = 35
		self.longPeriod = 3*self.Periodo

		self.Breve = self.periodiB
		self.Lunga = self.periodiL

		self.strategia = "-"


	# ========================= funzioni dell'algoritmo ========================= #
	def check_buy(self, t):
		#emacd = self.df['signal'][t]>self.df['macd'][t]
		#inclinazioneMACD = 35<self.df[f'inclinazione_perc{self.Periodo}'][t]<60 and 10<self.df[f'inclinazione_perc{self.longPeriod}'][t]<45
		inclinazioneBollinger = -10<self.df[f'inclinazione_perc{self.longPeriod}'][t] or True
		sar = self.df['psar_di'][t]==False
		aroon = self.df['aroon_indicator'][t]>-70
		if self.df[f'EMA{self.Breve}'][t]>self.df[f'EMA{self.Lunga}'][t]:
			sar = self.df['psar_di'][t]==False
			adxMACD = self.df['adx'][t]>20
			#emacd = self.df[f'EMA{self.Breve}'][t]>self.df[f'EMA{self.Lunga}'][t]
			if sar:
				self.strategia = "MACD"
		elif inclinazioneBollinger and sar and aroon:
			bollinger = self.df['bollinger_pband'][t]<0.2
			adx = self.df['adx'][t]>25
			if bollinger and adx:
				self.strategia = "BOLLINGER"
		return self.strategia != "-"

	def check_sell(self, t, entrata):
		if self.strategia == "MACD":
			if self.df[f'EMA{self.Breve}'][t]<self.df[f'EMA{self.Lunga}'][t] or self.stopCallMacd(t,entrata):
				self.strategia = "-"
		elif self.strategia == "BOLLINGER":
			if self.stopCallBollinger(t,entrata):
				self.strategia = "-"
		return self.strategia == "-"

	def stopCallMacd(self, t, entrata):
		sar = self.moltiplicatore*(self.df['Adj Close'][t]*(1-self.tassa)-entrata)/entrata>=0 and self.df['psar_di'][t]==True
		upper = self.df['Adj Close'][t]>entrata*(1+self.stopWinMACD)#*(1+self.df['atr_perc'][t]))
		lower = self.df['Adj Close'][t]<entrata*(1-self.stopLossMACD)#*(1+self.df['atr_perc'][t]))
		return upper or lower or sar

	def stopCallBollinger(self, t, entrata):
		sar = self.moltiplicatore*(self.df['Adj Close'][t]*(1-2*self.tassa)-entrata)/entrata>=0 and self.df['psar_di'][t]==True
		upper = self.df['Adj Close'][t]>entrata*(1+self.stopWinBollinger)#*(1+self.df['atr_perc'][t]))
		lower = self.df['Adj Close'][t]<entrata*(1-self.stopLossBollinger)#*(1+self.df['atr_perc'][t]))
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
		

	# ========================== funzioni statistiche ========================== #
	def plot3DGraph(self, nome, vec, show=False):
		X = linspace(1, self.periodiB-1, self.periodiB-1)
		Y = linspace(1, self.periodiL-1, self.periodiL-1)
		X, Y = meshgrid(X, Y)
		Z = array([[vec[b][l] for b in range(1,self.periodiB)] for l in range(1,self.periodiL)])

		# Data for a three-dimensional line
		plt.figure().clear()
		ax = plt.axes(projection='3d')
		if True:
			ax.plot_surface(X, Y, Z, rstride=1, cstride=1,
							cmap='viridis', edgecolor='none')
		else:
			ax.scatter(X, Y, Z, c=Z, cmap='viridis', linewidth=0.5);
		ax.set_title(nome)
		ax.set_xlabel('Breve')
		ax.set_ylabel('Lunga')
		if show:
			plt.show()
		else:
			plt.savefig(f"Img/{self.name}-{nome}.png")
		
	def findBest(self):
		best = -1
		bestb = -1
		bestl = -1
		for b in range(1,self.periodiB):
			for l in range(1,self.periodiL):
				if best < self.accuracy[b][l]:
					best = self.accuracy[b][l]
					bestb = b
					bestl = l
		return [bestb,bestl]

	def plotPrice(self, show=False):
		fig = plt.figure()
		gs = fig.add_gridspec(2, hspace=0, height_ratios=[3,1])
		axs = gs.subplots(sharex=True, sharey=False)
		axs[0].plot(self.df.index,self.df['Close'],'c',markersize=2)
		axs[0].plot(self.df.index,self.df.EMA20,'g',markersize=2)
		axs[0].plot(self.df.index,self.df.EMA70,'r',markersize=2)
		axs[1].plot(self.df.index,self.df.adx,'c',markersize=2)
		axs[0].label_outer()
		axs[1].label_outer()
		#plt.savefig(f"Img/{self.name}-{Breve}{Lunga}.png")
		plt.show()

	def printStatistics(self, s):
		b,l = s
		print(self.name,"-",b,l)
		print(f"Accuratezza: {self.accuracy[b][l]}")
		print(f"Corretti: {self.corretto[b][l]}")
		print(f"Sbagliati: {self.sbagliato[b][l]}")
		print(f"Guadagno Percentuale Medio: {self.guadagnoPercentualeMedio[b][l]}")
		print(f"Guadagno Percentuale: {self.guadagnoPercentuale[b][l]}")

	def drawStatistics(self, show=False):
		self.plot3DGraph("Accuratezza",self.accuracy,show)
		self.plot3DGraph("Guadagno",self.guadagnoPercentuale,show)