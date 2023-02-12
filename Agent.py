from time import sleep, time
import Strategy as StrategyLib
import Trader as TraderLib

class Agent:
	def __init__(self):
		self.exchange = "BTC"
		print("b1")
		self.Trader = TraderLib.Trader(self.exchange)
		print("b2")
		self.Strategy = StrategyLib.Strategy(self.exchange)
		print("b3")

		self.strategy = "-"

	def dentro(self):
		# NOTA: non c'e' una necessita' nel non mettere ordini contrastanti
		# visto che funzionano in parallelo, ma logicamente e' una buona idea, forse
		money,stocks = self.Trader.get_balance()
		long_position = self.Trader.lockedMoney!=0
		short_position = self.Trader.lockedStocks!=0
		return long_position or short_position

	def buy(self, short, trailing_delta):
		self.Trader.get_balance()
		spesa = self.Strategy.invest*self.Trader.money
		
		money,stocks = self.Trader.money,self.Trader.stocks
		result = self.Trader.openOrder(short,trailing_delta)
		k = 0
		MAX_k = 6
		while k<MAX_k:
			self.Trader.get_balance()
			# THIS MUST BE UPDATED WITH BETTER CONTROL
			# here I should check the buy and trailing stop order individually
			if self.Trader.lockedMoney!=0 or self.Trader.lockedStocks!=0:
				break
			sleep(10)
			k += 1
		if k==MAX_k:
			raise Exception("Oderd didn't go throught? Check.")

		if k==MAX_k:
			return [True,"Transaction had a problem. Check."]
		else:
			return [True,f"Strategy:{self.strategy}, result:{result}"] # da cambiare in self.strategy

	def check_buy(self, must_be_new=True):
		self.strategy, trailing_delta = self.Strategy.checkEnter(must_be_new)
		if not self.dentro() and self.strategy != "-":
			return self.buy("short" in self.strategy,trailing_delta)
		return [False,""]

	def updateData(self):
		self.Strategy.updateData()

	def actOnPosition(self, must_be_new=True):
		if not self.dentro():
			return self.check_buy(must_be_new=must_be_new)
		return [False,""]

	def get_total_balance(self):
		self.Trader.get_balance()
		return f"EUR: free({round(self.Trader.money,2)}€),locked({round(self.Trader.lockedMoney,2)}€)+(static{self.Trader.staticMoney}€)\n"+\
				f"Crypto: free({round(self.Trader.stocks,5)}{self.exchange}),locked({round(self.Trader.lockedStocks,5)}{self.exchange})+(static{round(self.Trader.staticCrypto,5)}{self.exchange})\n"+\
				f"Price: {self.Trader.get_price()}{self.exchange}/€\n"+\
				f" Total({self.exchange}+EUR): {round(self.Trader.money+self.Trader.lockedMoney+self.Trader.get_price()*(self.Trader.stocks+self.Trader.lockedStocks),5)}€"

	def get_current_state(self, data):
		#self.Strategy.updateData() low priority call
		return "no flags described"
