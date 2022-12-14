import discord
from discord.ext import commands
import asyncio
from time import time
from datetime import datetime, timedelta
import Agent as AgentLib
import Clock as ClockLib

class Bot:
	def __init__(self):
		self.client = discord.Client()
		self.Agent = AgentLib.Agent()
		self.Clock = ClockLib.Clock(interval=self.Agent.Strategy.interval)
		self.name = f"{self.Clock.get_time_id()}"
		self.SESSION = "run"

		# id canali
		self.room = {'generaleCH':1005242726125678635,
						'attivitaCH':1005245873883713546,
						'datiCH':1005255394710528162,
						'transazioniCH':1005968395927293962,
						'azioniCH':1005245915931615393,
						'bookCH':1017463347026858134,
						'spamCH':1022115220031811685}


	async def startConnectionMessage(self):
		greet_message = "Starting Connection."
		await self.client.get_channel(self.room['attivitaCH']).send(greet_message)

	async def crashMessage(self,e):
		allowed_mentions = discord.AllowedMentions(everyone = True)
		await self.client.get_channel(self.room['azioniCH']).send(content=str(e), allowed_mentions=allowed_mentions)

	async def runLoop(self):
		self.Clock.sleep()
		await self.client.get_channel(self.room['attivitaCH']).send(f"Connection check({self.Clock.time()}).")
		#data = get_data(Agent.currentName)
		#info0 = data.iloc[-1]
		#await self.client.get_channel(datiCH).send(f"[{Agent.exchange}] {info0.name}| Open:{info0['Open']}/Low:{info0['Low']}/High:{info0['High']}/Close:{info0['Close']}")
		print(">>>",self.Agent.actOnPosition())
		flag, r = self.Agent.actOnPosition()
		print(self.Agent.dentro)
		if flag and False:
			# Transaction message
			await self.client.get_channel(self.room['transazioniCH']).send(r)
			# Action message
			allowed_mentions = discord.AllowedMentions(everyone = True)
			await self.client.get_channel(self.room['azioniCH']).send(content="@everyone Stock transaction happened.", allowed_mentions=allowed_mentions)
			r = self.Agent.get_current_state(data)
			await self.client.get_channel(self.room['azioniCH']).send(r)
		