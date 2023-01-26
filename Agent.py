from time import sleep, time
import Strategy as StrategyLib
import Trader as TraderLib

DEFAULT_TRAILING_DELTA = 0.01

class Agent:
	def __init__(self):
		self.exchange = "BTC"
		print("b1")
		self.Trader = TraderLib.Trader(self.exchange)
		print("b2")
		self.Strategy = StrategyLib.Strategy(self.exchange)
		print("b3")
		
		self.strategy = "-"

		self.entrata = 0
		self.ora = 0
		self.shorting = False

	def dentro(self):
		money,stocks = self.Trader.get_balance()
		price = self.Trader.get_price()
		long_position = money<5
		short_position = stocks<0
		return long_position or short_position

	def buy(self, short=False, trailing_delta=DEFAULT_TRAILING_DELTA):
		self.ora = int((time()-60)*1000)
		self.Trader.get_balance()
		spesa = self.Strategy.invest*self.Trader.money
		
		money,stocks = self.Trader.money,self.Trader.stocks
		result = self.Trader.openOrder(short,trailing_delta)
		k = 0
		MAX_k = 6
		while k<MAX_k:
			self.Trader.get_balance()
			# if they changes by more than 10%
			if abs(money-self.Trader.money)/money > 0.1 and abs(stocks-self.Trader.stocks)/stocks > 0.1:
				break
			sleep(10)

		if k==MAX_k:
			return [False,"Transaction had a problem."]
		else:
			return [True,f"Strategy:{self.strategy}, result:{result}"] # da cambiare in self.strategy

	def check_buy(self, forced=False, forced_short=False, must_be_new=True):
		self.strategy, trailing_delta = self.Strategy.checkEnter(must_be_new)
		if not self.dentro() and (self.strategy != "-" or forced):
			if self.strategy != "-":
				return self.buy("short" in self.strategy,trailing_delta)
			elif forced:
				return self.buy(forced_short)
		return [False,""]

	# this method is invoked only as a force sell
	def sell(self):
		#output = self.closeOrder() # <- to activate
		return [True,"Tried selling?"]
		#return [True,f"Exit: Crypto:{self.stocks} {self.currentName} / Balance:{round(self.money,2)}$ || {output}"]

	def updateData(self):
		self.Strategy.updateData()

	def actOnPosition(self, must_be_new=True):
		if not self.dentro():
			return self.check_buy(forced=False,forced_short=False,must_be_new=must_be_new)
		else:
			return self.Strategy.actOnOpenPosition()
		return [False,""] # This should not be executed

	def get_total_balance(self):
		self.Trader.get_balance()
		return f"Balance: {self.Trader.money}€+(static{self.Trader.staticMoney}€) /"+\
				f" Crypto: {self.Trader.stocks}{self.exchange}({self.Trader.get_price()*self.Trader.stocks}€)"+\
				f"({self.Trader.get_price()}ETH/€) /"+\
				f" Total(ETH+BUSD): {self.Trader.money+self.Trader.get_price()*self.Trader.stocks}€"

	def get_current_state(self, data):
		#self.Strategy.updateData() low priority call
		return "no flags described"
