from time import sleep, time
import Strategy as StrategyLib
import Trader as TraderLib

class Agent:
	def __init__(self):
		self.exchange = "ETH"
		self.Trader = TraderLib.Trader(self.exchange)
		self.Strategy = StrategyLib.Strategy(self.exchange)
		
		self.strategy = "-"

		self.dentro = False
		self.entrata = 0
		self.ora = 0
		self.shorting = False

	def buy(self, short=False):
		self.ora = int((time()-60)*1000)
		self.Trader.get_balance()
		spesa = self.Strategy.invest*self.Trader.money
		strategy = self.strategy
		self.strategy = "-" # Da togliere
		# self.dentro = True e' commentato, prendo tutti i segnali
		"""if  and False: # <- to activate
			self.shorting = True

		r = 0#self.Trader.enterOrder(fraction=self.Strategy.invest,sl=sl,tp=tp)

		#if self.Trader.openOrder()
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
		
		time.sleep(30)
		self.Trader.get_balance()"""
		# sostituire con una call per vedere gli ordini aperti
		return [True,f"{strategy} (Close:{self.Strategy.df.Close.iloc[-1]}), sl:{self.Strategy.df.Close.iloc[-1]*0.98}, tp:{self.Strategy.df.Close.iloc[-1]*(1+0.02*1.5)}"] # da cambiare in self.strategy

	def check_buy(self, forced=False, forced_short=False):
		self.strategy, sl, tp = self.Strategy.checkEnter()
		if not self.dentro and (self.strategy != "-" or forced):
			if self.strategy != "-":
				return self.buy("short" in self.strategy)
			elif forced:
				return self.buy(forced_short)
		return [False,""]

	# this method is invoked only as a force sell
	def sell(self):
		#output = self.closeOrder() # <- to activate
		return [True,"a"]
		#return [True,f"Exit: {self.get_price()}"]
		#return [True,f"Exit: Crypto:{self.stocks} {self.currentName} / Balance:{round(self.money,2)}$ || {output}"]

	def updateData(self):
		self.Strategy.updateData()

	def actOnPosition(self):
		if not self.dentro:
			return self.check_buy()
		else:
			return self.Strategy.actOnOpenPosition()
		return [False,""] # This should not be executed

	def get_total_balance(self):
		return "some number"
		"""self.Trader.get_balance()
		return f"Balance: {self.Trader.money}$+({self.Trader.staticMoney}$) /"+\
				f" Crypto: {self.stocks}{self.currentName}({self.get_price()*self.stocks}$)({self.get_price()}ETH/$) /"+\
				f" Total(ETH+BUSD): {self.money+self.get_price()*self.stocks}$ /Homecash: {self.euro}€"
		"""
	def get_current_state(self, data):
		#self.Strategy.updateData() low priority call
		return "no flags described"
