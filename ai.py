class AI:
	def __init__(self):
		pass

	def eval(self,df,t):
		if random()>0.1:
			return "random",[-100,-100]
		return "-",[-100,-100]
