# Service that manage the discord bot
# Sonoda 10/12/2022

import traceback
import os
import asyncio
import Bot as BotLib

print("Starting program...")
bot = BotLib.Bot()
print(bot.name)

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
	await bot.client.close()


@bot.client.event
async def on_message(message):
	print(1)
	if message.author == bot.client.user:
		return
	print(2,bot.name)
	if message.content == "kill "+bot.name:
		bot.SESSION = "exit"
	# da rendere migliore
	await message.channel.send(f"[{bot.name}] Received: {message.content}")

	# dividere comandi tell and do <--

	if message.channel.id==bot.room['azioniCH']:
		# Temporary offline-mode
		if message.content=="shutdown" or message.content=="s":
			bot.SESSION = not bot.SESSION
			await message.channel.send(f"Execution is now set to {bot.SESSION}")
		# Terminating program
		# elif message.content=="ss":
		# 	bot.SESSION = -1
		# 	await bot.client.close()
		# # Help command
		elif message.content=="help" or message.content=="h":
			await message.channel.send(f"help-h\nshutdown-s\nbalance-b\ncancel(orders)\ncurrent orders\nhistory\nmanualBuy <eur>\nmanualSell <crypto>\ncs (current state)\nmanual long trailing stop <quantity>\nmanual short trailing stop <quantity>\ntry checking now")
		# # Version command
		# elif message.content=="version" or message.content=="v":
		# 	await message.channel.send(f"B2.0.0")
		# # Modify state, enter->exit, or exit->enter
		# elif message.content=="enter" or message.content=="exit" or message.content=="e":
		# 	Agent.dentro = not Agent.dentro
		# 	await message.channel.send(f"Stato corrente aggiornato: dentro={Agent.dentro}") # <-
		# # Modify entry price value
		# elif message.content=="entrata":
		# 	Agent.entrata = message.content.split(" ")[1]
		# # Get balance command
		elif message.content=="balance" or message.content=="b":
			await message.channel.send(bot.Agent.get_total_balance())
		elif message.content=="cancel":
			await message.channel.send(bot.Agent.Trader.cancel_open_orders())
		elif message.content=="current orders":
			await message.channel.send(bot.Agent.Trader.get_current_open_orders())
		elif message.content=="history":
			await message.channel.send(bot.Agent.Trader.get_trade_history())
		elif message.content.split(" ")[0]=="manualBuy":
			await message.channel.send(bot.Agent.Trader.manual_buy_amount(float(message.content.split(" ")[1])))
		elif message.content.split(" ")[0]=="manualSell":
			await message.channel.send(bot.Agent.Trader.manual_sell_amount(float(message.content.split(" ")[1])))
		elif " ".join(message.content.split(" ")[:-1])=="manual long trailing stop":
			await message.channel.send(bot.Agent.Trader.manual_long_trailing_stop(float(message.content.split(" ")[-1])))
		elif " ".join(message.content.split(" ")[:-1])=="manual short trailing stop":
			await message.channel.send(bot.Agent.Trader.manual_short_trailing_stop(float(message.content.split(" ")[-1])))			
		elif message.content=="cs":
			await message.channel.send(bot.Agent.Strategy.get_current_state())
		elif message.content=="try checking now":
			await message.channel.send(bot.Agent.Strategy.get_current_state())
			transaction_happened, r = bot.Agent.actOnPosition(must_be_new=False)
			await message.channel.send(f"Transaction happening: {transaction_happened}")
			if transaction_happened:
				# Transaction message
				await self.client.get_channel(self.room['transazioniCH']).send(f"[{self.name}] "+r)
				# Action message
				allowed_mentions = discord.AllowedMentions(everyone = True)
				await self.client.get_channel(self.room['azioniCH']).send(content=f"[{self.name}] @everyone Stock transaction happened.", allowed_mentions=allowed_mentions)

		# Get flags for state
		# elif message.content=="state" or message.content=="c": # c di current state
		# 	r = Agent.get_current_state(get_data(Agent.currentName))
		# 	await message.channel.send(r)
		# Force a buy command
		# elif "force enter" in message.content:
		# 	if len(message.content.split(" "))==3:
		# 		flag, r = Agent.buy(datetime.fromtimestamp(time()).strftime("%H:%M:%S"),get_data(Agent.currentName),forced=True)
		# 		if flag:
		# 			await bot.client.get_channel(transazioniCH).send(r)
		# 	# Buy short
		# 	elif len(message.content.split(" "))==4:
		# 		flag, r = Agent.buy(datetime.fromtimestamp(time()).strftime("%H:%M:%S"),get_data(Agent.currentName),forced=True,short=True)
		# 		if flag:
		# 			await bot.client.get_channel(transazioniCH).send(r)
		# # Force a sell command
		# elif message.content=="force exit":
		# 	flag, r = Agent.sell(datetime.fromtimestamp(time()).strftime("%H:%M:%S"),get_data(Agent.currentName),True)
		# 	if flag:
		# 		await bot.client.get_channel(transazioniCH).send(r)


#Bottom of Main.py
bot.client.run(os.environ['DISCORD_TOKEN'])
