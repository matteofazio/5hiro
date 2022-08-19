from numpy import arctan
from ta.trend import *
from ta.momentum import *
from ta.volatility import *
from algorithmETH import AlgorithmETH

class AGENT:
	def __init__(self):
		# parametri
		self.tassa = 0.0054
		self.moltiplicatore = 5
		self.stocks = 0
		self.invest = 1 # 100%

		# algoritmi
		self.ETH = AlgorithmETH(self.tassa,self.moltiplicatore)
		#self.DOGE = AlgorithmDOGE(self.tassa,self.moltiplicatore)
		self.A = [self.ETH]

		# statistiche
		self.moneyT = []
		self.transactionTime = []

		# Parametri della simulazione
		self.money = 50
		self.dentro = False
		self.prestito = 0
		self.spesa = 0
		self.entrata = 0

		self.strategia = "-"
		self.current = -1
		self.currentName = ["ETH"]
		self.currentNameResult = ["XETHZ"]

	# ========================= funzioni di gestione ========================= #
	def buy(self, now, data, forced=False, which=-1):
		self.A[0].df = data[0].astype(float)
		self.A[0].analyzeDf()
		if (not self.dentro and self.A[0].check_buy(-1) == True):
			self.current = 0
			self.spesa = min(self.invest*self.money, self.money)
			self.money -= self.spesa
			prestito = (self.moltiplicatore-1)*self.spesa
			self.stocks += (1-self.tassa/2)*(self.spesa+prestito)/self.A[self.current].df['Close'][-1]
			self.prestito += prestito
			self.entrata = self.A[self.current].df['Close'][-1]
			self.dentro = True
			self.transactionTime.append(now)
			self.moneyT.append(self.money)
			return [True,f"Buy: Crypto:{self.stocks} {self.currentName[self.current]}({self.spesa}+{self.prestito}={self.spesa+self.prestito}€) / Balance:{self.money}€"]
		elif forced:
			self.current = which
			self.spesa = min(self.invest*self.money, self.money)
			self.money -= self.spesa
			prestito = (self.moltiplicatore-1)*self.spesa
			self.stocks += (1-self.tassa/2)*(self.spesa+prestito)/self.A[self.current].df['Close'][-1]
			self.prestito += prestito
			self.entrata = self.A[self.current].df['Close'][-1]
			self.dentro = True
			self.transactionTime.append(now)
			self.moneyT.append(self.money)
			return [True,f"Buy: Crypto:{self.stocks} {self.currentName[self.current]}({self.spesa}+{self.prestito}={self.spesa+self.prestito}€) / Balance:{self.money}€"]
		return [False,""]

	def sell(self, now, data, forced=False):
		self.A[0].df = data[0].astype(float)
		self.A[0].analyzeDf()
		if (self.dentro and self.A[self.current].check_sell(-1, self.entrata) == True) or forced:
			self.dentro = False
			self.money += round((1-self.tassa/2)*self.stocks*self.A[self.current].df['Close'][-1]-self.prestito*(1-self.tassa/2),2)
			self.prestito = 0
			self.stocks = 0
			self.transactionTime.append(now)
			self.moneyT.append(self.money)
			m = self.current
			self.current = -1
			return [True,f"Sell: Crypto:{self.stocks} {self.currentName[m]} / Balance:{round(self.money,2)}€"]
		return [False,""]


	def set(self, v):
		if len(v)!=2:
			return 0

		if v[0] == "money":
			self.money = float(v[1])

	def show_settings(self):
		return f"Money={self.money}€"

	def get_current_state(self, data):
		self.A[0].df = data[0].astype(float)
		self.A[0].analyzeDf()

		return f"{self.currentName[0]}: EMAb={round(self.A[0].df[f'EMA{self.A[0].periodiB}'][-1],2)} / EMAl={round(self.A[0].df[f'EMA{self.A[0].periodiL}'][-1],2)} / Psar>={self.A[0].df['psar_di'][-1]} / ADX={round(self.A[0].df['adx'][-1],2)} / Aroon={round(self.A[0].df['aroon_indicator'][-1],2)} / Bollinger={self.A[0].df['bollinger_pband'][-1]}"
