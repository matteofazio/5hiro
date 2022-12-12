from time import time, sleep
from datetime import datetime, timedelta

class Clock:
	def __init__(self,interval=5):
		# time parameters
		self.interval = interval
		self.intervalTime = 5 # minuti

	def sleep(self):
		now = [int(i) for i in datetime.fromtimestamp(time()).strftime("%H:%M:%S").split(":")]
		if self.interval == 5: # 5 minutes
			minutes = now[1]%5
			secondsToSleep = (5-minutes)*60
			secondsToSleep += 20-now[2] # 20 seconds after the 5 minutes
		if self.interval == 1:
			minutes = now[1]
			secondsToSleep = (60-minutes)*60
			secondsToSleep += 20-self.now[2]  # 20 seconds after the 1 hour
		print(secondsToSleep)
		sleep(secondsToSleep)
		self.now = datetime.fromtimestamp(time()).strftime("%H:%M:%S").split(":")

	def time(self):
		return ":".join(datetime.fromtimestamp(time()).strftime("%H:%M:%S").split(":")[:-1])