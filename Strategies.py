import pandas as pd
import os
from random import random
from time import gmtime, mktime
from ta.trend import *
from ta.momentum import *
from ta.volatility import *
import talib


class StrategyManager:
	def __init__(self):
		self.LBBP = Lbbp()
		self.SBBP = Sbbp()

	def checkSignal(self,df):
		if self.LBBP.isLong(df):
			return "longbbp", self.LBBP
		if self.SBBP.isShort(df):
			return "shortbbp", self.SBBP
		return "-", 0.1

class Lbbp:
	def __init__(self):
		self.sl = round(0.009178993650693367,2)
		self.ratio = 7
		self.param = 0.1260629959007512

	def isLong(self,df):
		longCondition = df["bbp"].iloc[-1]<self.param
		return longCondition

class Sbbp:
	def __init__(self):
		self.sl = round(0.003689112508705772,2)
		self.ratio = 6
		self.param = 0.9018492259911476

	def isShort(self,df):
		shortCondition = df["bbp"].iloc[-1]>self.param
		return shortCondition
