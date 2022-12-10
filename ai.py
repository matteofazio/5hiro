from cryptography.fernet import Fernet
from random import random

class Model:
	def __init__(self, name, ranges):
		self.N = len(ranges)
		self.ranges = ranges
		self.bubbles = []
		self.fillBubbles(name)

	def fillBubbles(self, name):
		f = open(name,"rb")
		key = "nelJ4yFu7AEWZvQWHv_1ce-EFQTOnNtDsCtLiT4GR5g="
		fernet = Fernet(key)
		lines = fernet.decrypt(f.read()).decode("utf-8").split("\n")
		line = 0
		for i in lines:
			try:
				self.bubbles.append([float(j) for j in i.split(" ")])
			except Exception:
				pass

	def eval(self, state):
		for b in self.bubbles:
			# for each bubble
			flag = True
			for i in range(len(state)):
				# for each coordinate
				if abs(state[i]-b[i])>=self.ranges[i]:
					flag = False
					break
			if flag == True:
				return True,[b[-2],b[-1]]
		return False,[]

class AI:
	def __init__(self):
		self.macd = Model("_macd.md",[0.2,0.02,2])
		self.bollinger = Model("_bollinger.md",[0.01,0.1,1])

	def inclination(self,df,t,who,span):
		return (df[who].iloc[t]-df[who].iloc[t-span])/span

	def eval(self,df,t):
		# MACD
		evaluation,calls = self.macd.eval([df['macd_diff'].iloc[t],df['distance'].iloc[t],df['rocEMA100'].iloc[t]])
		if evaluation:
			return "MACD",calls
		# bollinger
		evaluation,calls = self.bollinger.eval([df['bollinger_pband'].iloc[t],df['distance'].iloc[t],df['bollinger_wband'].iloc[t]])
		if evaluation:
			return "bollinger",calls

		# test
		#evaluation,calls = self.bollinger.eval([df['bollinger_pband'].iloc[t],df['distance'].iloc[t],df['bollinger_wband'].iloc[t]])
		if random()>0.1:
			return "random",[-100,-100]
		return "-",[-100,-100]
