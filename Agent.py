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

	def buy(self, forced=False, short=False):
		self.strategy, sl, tp = self.Strategy.checkEnter()
		if not self.dentro and self.strategy != "-":
			self.ora = int((time()-60)*1000)
			self.Trader.get_balance()
			spesa = self.Strategy.invest*self.money
			if "short" in self.strategy and False: # <- to activate
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
			self.Trader.get_balance()
			return [True,r]
			#return [True,f"Enter: {self.get_price()} [{self.A.strategia}]"]
			#return [True,f"[{self.A.strategia}] Enter: Crypto:{self.stocks} {self.currentName}({costo}*{self.moltiplicatore}={costo*self.moltiplicatore}$) / Balance:{self.money}$ || {output}"]
		elif forced:
			self.Trader.get_balance()
			spesa = self.invest*self.money
			if short==True:
				self.shorting = True
			output = self.enter_order()
			r = 0
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
			self.Trader.get_balance()
			return [True,r]
			#return [True,f"[{self.A.strategia}] Enter: Crypto:{self.stocks} {self.currentName}({costo}*{self.moltiplicatore}={costo*self.moltiplicatore}$) / Balance:{self.money}$ || {output}"]
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
			return self.buy()
		else:
			return self.Strategy.actOnOpenPosition()

	def get_total_balance(self):
		"""self.Trader.get_balance()
		return f"Balance: {self.Trader.money}$+({self.Trader.staticMoney}$) /"+\
				f" Crypto: {self.stocks}{self.currentName}({self.get_price()*self.stocks}$)({self.get_price()}ETH/$) /"+\
				f" Total(ETH+BUSD): {self.money+self.get_price()*self.stocks}$ /Homecash: {self.euro}€"
		"""
	def get_current_state(self, data):
		#self.Strategy.updateData() low priority call
		return "no flags described"
