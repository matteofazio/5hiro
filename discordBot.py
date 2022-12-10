import discord
from discord.ext import commands
import asyncio
from yfinance import download
from requests import get
from time import time, sleep
from pandas import DataFrame, to_datetime, concat
from datetime import datetime
from math import floor
from agent import AGENT
import os
from yfinance import download
from datetime import datetime, timedelta

client = discord.Client()
SESSION = True
Last_update = datetime.fromtimestamp(time()).strftime("%H:%M:%S")
Last_minute = -1
Agent = AGENT()

# id canali
generaleCH = 1005242726125678635
attivitaCH = 1005245873883713546
datiCH = 1005255394710528162
transazioniCH = 1005968395927293962
azioniCH = 1005245915931615393
bookCH = 1017463347026858134
spamCH = 1022115220031811685

# statistiche varie
bookValues = []
ohlc = []

def check_time():
	global Last_update
	now = datetime.fromtimestamp(time()).strftime("%H:%M:%S").split(":")
	soglia = Last_update.split(":")
	now = [int(i) for i in now]
	soglia = [int(i) for i in soglia]
	if 2<now[1]<10 and now[0]>=(soglia[0]+1)%24:
		Last_update = datetime.fromtimestamp(time()).strftime("%H:%M:%S")
		return True
	return False


def get_data(asset):
	SPAN = 500 # < 720
	i = 0
	while i<10:
		data = download(f"{asset}-EUR", start=datetime.now()-timedelta(hours=500), end=datetime.now(), interval="1h", auto_adjust=False, prepost=False).astype(float).sort_index()
		if data.iloc[-1]['Open'] == data.iloc[-1]['Close']:
			break
		i += 1
		sleep(10)
	return data.iloc[:-1]

def process_data(data):
	if not Agent.dentro:
		return Agent.buy(datetime.fromtimestamp(time()).strftime("%H:%M:%S"), data)
	else:
		return Agent.sell(datetime.fromtimestamp(time()).strftime("%H:%M:%S"), data)


@client.event
async def on_ready():
	for guild in client.guilds:

		print(
			f'{client.user} is connected to the following guild:\n'
			f'{guild.name}(id: {guild.id})'
		)


	await client.get_channel(attivitaCH).send("Starting Connection.")
	global SESSION
	while True:
		if SESSION==True:
			try:
				await asyncio.sleep(30)
				if check_time():
					now = datetime.fromtimestamp(time()).strftime("%H:%M")
					await client.get_channel(attivitaCH).send(f"Connection check({now}).")
					data = get_data(Agent.currentName)
					info0 = data.iloc[-1]
					await client.get_channel(datiCH).send(f"{Agent.currentName}:{info0.name}| Open:{info0['Open']}/Low:{info0['Low']}/High:{info0['High']}/Close:{info0['Close']}")
					flag, r = process_data(data)
					if flag:
						# Transaction message
						await client.get_channel(transazioniCH).send(r)
						# Action message
						allowed_mentions = discord.AllowedMentions(everyone = True)
						await client.get_channel(azioniCH).send(content="@everyone Stock transaction happened.", allowed_mentions=allowed_mentions)
						r = Agent.get_current_state(data)
						await client.get_channel(azioniCH).send(r)
					
			except Exception as e:
				print(e)
				allowed_mentions = discord.AllowedMentions(everyone = True)
				await client.get_channel(azioniCH).send(content=str(e), allowed_mentions=allowed_mentions)

		elif SESSION==False:
			try:
				await asyncio.sleep(100)
			except Exception as e:
				print(e)
		elif SESSION==-1:
			break


@client.event
async def on_message(message):
	global SESSION
	if message.author == client.user:
		return

	# dividere comandi tell and do <--

	if message.channel.id==azioniCH:
		# Temporary offline-mode
		if message.content=="shutdown" or message.content=="s":
			SESSION = not SESSION
			await message.channel.send(f"Execution is now set to {SESSION}")
		# Terminating program
		elif message.content=="ss":
			SESSION = -1
			await client.close()
		# Help command
		elif message.content=="help" or message.content=="h":
			await message.channel.send(f"help-h\nversion-v\nshutdown/execute-s\nbalance-b\nstate-c\nforce buy 0\nforce sell\nbook\nenter/exit e")
		# Version command
		elif message.content=="version" or message.content=="v":
			await message.channel.send(f"B1.2.0")
		# Modify state, enter->exit, or exit->enter
		elif message.content=="enter" or message.content=="exit" or message.content=="e":
			Agent.dentro = not Agent.dentro
			await message.channel.send(f"Stato corrente aggiornato: dentro={Agent.dentro}") # <-
		# Modify entry price value
		elif message.content=="entrata":
			Agent.entrata = message.content.split(" ")[1]
		# Get balance command
		elif message.content=="balance" or message.content=="b":
			await message.channel.send(Agent.get_total_balance())
		# Get flags for state
		elif message.content=="state" or message.content=="c": # c di current state
			r = Agent.get_current_state(get_data(Agent.currentName))
			await message.channel.send(r)
		# Force a buy command
		elif "force enter" in message.content:
			if len(message.content.split(" "))==3:
				flag, r = Agent.buy(datetime.fromtimestamp(time()).strftime("%H:%M:%S"),get_data(Agent.currentName),forced=True)
				if flag:
					await client.get_channel(transazioniCH).send(r)
			# Buy short
			elif len(message.content.split(" "))==4:
				flag, r = Agent.buy(datetime.fromtimestamp(time()).strftime("%H:%M:%S"),get_data(Agent.currentName),forced=True,short=True)
				if flag:
					await client.get_channel(transazioniCH).send(r)
		# Force a sell command
		elif message.content=="force exit":
			flag, r = Agent.sell(datetime.fromtimestamp(time()).strftime("%H:%M:%S"),get_data(Agent.currentName),True)
			if flag:
				await client.get_channel(transazioniCH).send(r)

client.run(os.environ['DISCORD_TOKEN'])
