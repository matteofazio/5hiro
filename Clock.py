from time import time, sleep
import asyncio
from datetime import datetime, timedelta

class Clock:
	def __init__(self,interval=5):
		# time parameters
		self.interval = interval
		self.intervalTime = 5 # minuti

	async def sleep(self):
		now = [int(i) for i in datetime.fromtimestamp(time()).strftime("%H:%M:%S").split(":")]
		if self.interval == "5m": # 5 minutes
			minutes = now[2]%5
			secondsToSleep = (5-minutes)*60
			secondsToSleep += 7-now[2] # 20 seconds after the 5 minutes
		elif self.interval == "1h":
			minutes = now[1]
			secondsToSleep = (60-minutes)*60
			secondsToSleep += 20-now[2]  # 20 seconds after the 1 hour
		await asyncio.sleep(secondsToSleep)
		self.now = datetime.fromtimestamp(time()).strftime("%H:%M:%S").split(":")

	def get_time_id(self):
		return int(time())

	def time(self):
		return ":".join(datetime.fromtimestamp(time()).strftime("%H:%M:%S").split(":")[:-1])