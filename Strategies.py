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
		self.BBP = bbp()
		self.BBP2 = bbp2()
		self.SAR = sar()
		self.ROCENGULFING = RocEngulfing()
		self.DEMA = dema()

	def checkSignal(self,df):
		if self.BBP.isLong(df):
			return "longbbp", self.BBP.sl
		if self.BBP.isShort(df):
			return "shortbbp", self.BBP.sl
		if self.SAR.isLong(df):
			return "longSar", self.SAR.sl
		if self.SAR.isShort(df):
			return "shortSar", self.SAR.sl
		if self.BBP2.isLong(df):
			return "longbbp2", self.BBP2.sl
		if self.BBP2.isShort(df):
			return "shortbbp2", self.BBP2.sl
		return "-", 0.1

class bbp:
	def __init__(self):
		self.sl = round(0.32802163381592904,2)
		self.Blong = 0.4892580621824426
		self.Llong = 0.020687689682924018
		self.Bshort = 0.7468307530491093
		self.Lshort = 0.2506131107807094

	def isLong(self,df):
		longCondition = self.Llong<df["bbp"].iloc[-1]<self.Blong
		return longCondition

	def isShort(self,df):
		shortCondition = self.Lshort<df["bbp"].iloc[-1]<self.Bshort
		return shortCondition


class bbp2:
	def __init__(self):
		self.sl = round(0.3115424563109974,2)
		self.Blong = 0.5196623142934206
		self.Llong = -0.23183882344423917
		self.Bshort = 1.002747193727743
		self.Lshort = 0.7596422157283184

	def isLong(self,df):
		longCondition = self.Llong<df["bbp"].iloc[-1]<self.Blong
		return longCondition

	def isShort(self,df):
		shortCondition = self.Lshort<df["bbp"].iloc[-1]<self.Bshort
		return shortCondition

class sar:
	def __init__(self):
		self.sl = round(0.37539724869033748,2)
		self.Blong = 2.8913845534412097
		self.Llong = 2.0450698966405807
		self.Bshort = 2.8284570290582782
		self.Lshort = -0.40812637390980633

	def isLong(self,df):
		longCondition = self.Llong<df["sar"].iloc[-1]<self.Blong
		return longCondition

	def isShort(self,df):
		shortCondition = self.Lshort<df["sar"].iloc[-1]<self.Bshort
		return shortCondition


class RocEngulfing:
	def __init__(self):
		self.sl = 2.2
		self.Blong = 4.543934569468048
		self.Llong = 0.2826642081488359
		self.Bshort = 7.983638591633049
		self.Lshort = 0.21102464612608376

		self.longEngulfing = -100
		self.shortEngulfing = 100

	def isLong(self,df):
		longCondition = self.Llong<df["roc"].iloc[-1]<self.Blong and df["CDLENGULFING"].iloc[-1]==self.longEngulfing
		return longCondition

	def isShort(self,df):
		shortCondition = self.Lshort<df["roc"].iloc[-1]<self.Bshort and df["CDLENGULFING"].iloc[-1]==self.shortEngulfing
		return shortCondition


class dema:
	def __init__(self):
		self.sl = round(0.6169963141013897,2)
		self.Blong = 2.606635068781724
		self.Llong = -0.26920982264089943
		self.Bshort = 7.631625104740909
		self.Lshort = -8.420778440769862

	def isLong(self,df):
		longCondition = self.Llong<df["dema"].iloc[-1]<self.Blong
		return longCondition

	def isShort(self,df):
		shortCondition = self.Lshort<df["dema"].iloc[-1]<self.Bshort
		return shortCondition
