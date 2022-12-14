# Service that manage the discord bot
# Sonoda 10/12/2022

import traceback
import os
import Bot as BotLib
from webserver import keep_alive


bot = BotLib.Bot()

@bot.client.event
async def on_ready():
	for guild in bot.client.guilds:
		print(
			f'{bot.client.user} is connected to the following guild:\n'
			f'{guild.name}(id: {guild.id})'
		)

	await bot.startConnectionMessage()
	while True:
		# running mode
		if bot.SESSION=="run":
			try:
				await bot.runLoop()
			except Exception as e:
				print(e)
				print(traceback.format_exc())
				await bot.crashMessage(traceback.format_exc())
		# sleep mode
		elif bot.SESSION=="sleep":
			try:
				await asyncio.sleep(100)
			except Exception as e:
				print(e)
				await bot.crashMessage(e)
		# end program
		elif bot.SESSION=="exit":
			break


@bot.client.event
async def on_message(message):
	if message.author == bot.client.user:
		return

	# da rendere migliore
	await message.channel.send(f"Received: {message.content}")
	return
	# dividere comandi tell and do <--

	if message.channel.id==azioniCH:
		# Temporary offline-mode
		if message.content=="shutdown" or message.content=="s":
			bot.SESSION = not bot.SESSION
			await message.channel.send(f"Execution is now set to {bot.SESSION}")
		# Terminating program
		elif message.content=="ss":
			bot.SESSION = -1
			await bot.client.close()
		# Help command
		elif message.content=="help" or message.content=="h":
			await message.channel.send(f"help-h\nversion-v\nshutdown/execute-s\nbalance-b\nstate-c\nforce buy 0\nforce sell\nbook\nenter/exit e")
		# Version command
		elif message.content=="version" or message.content=="v":
			await message.channel.send(f"B2.0.0")
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
					await bot.client.get_channel(transazioniCH).send(r)
			# Buy short
			elif len(message.content.split(" "))==4:
				flag, r = Agent.buy(datetime.fromtimestamp(time()).strftime("%H:%M:%S"),get_data(Agent.currentName),forced=True,short=True)
				if flag:
					await bot.client.get_channel(transazioniCH).send(r)
		# Force a sell command
		elif message.content=="force exit":
			flag, r = Agent.sell(datetime.fromtimestamp(time()).strftime("%H:%M:%S"),get_data(Agent.currentName),True)
			if flag:
				await bot.client.get_channel(transazioniCH).send(r)


#Bottom of Main.py

keep_alive()
bot.client.run(os.environ['DISCORD_TOKEN'])
