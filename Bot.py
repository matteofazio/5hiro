import discord
from discord.ext import commands
import asyncio
from time import time
from datetime import datetime, timedelta
import Agent as AgentLib
import Clock as ClockLib

class Bot:
	def __init__(self):
		print("a")
		self.client = discord.Client()
		print("b")
		self.Agent = AgentLib.Agent()
		print("c")
		self.Clock = ClockLib.Clock(interval=self.Agent.Strategy.interval)
		print("d")
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
		await self.Clock.sleep()
		if self.SESSION != "run":
			return
		await self.client.get_channel(self.room['attivitaCH']).send(f"Connection check({self.Clock.time()}).")
		# print current situation every hour
		await self.client.get_channel(self.room['azioniCH']).send(self.Agent.Strategy.get_current_state())
		transaction_happened, r = self.Agent.actOnPosition()
		if transaction_happened:
			# Transaction message
			await self.client.get_channel(self.room['transazioniCH']).send(f"[{self.name}] "+r)
			# Action message
			allowed_mentions = discord.AllowedMentions(everyone = True)
			await self.client.get_channel(self.room['azioniCH']).send(content=f"[{self.name}] @everyone Stock transaction happened.", allowed_mentions=allowed_mentions)
