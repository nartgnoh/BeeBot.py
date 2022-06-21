# *********************************************************************************************************************
# pollsmodule.py
# - poll command
# - giveaway command (wip)
# *********************************************************************************************************************

import os
import discord
import cogs.helper.constants.emoji_constants as emoji_constants

from discord.ext import commands
from discord.ext.commands import Cog
from discord import Embed
from typing import Optional
from datetime import datetime, timedelta

# role specific names
role_specific_command_name = 'Bot Commander'
admin_specific_command_name = 'Bot Admin'

# pollsmodule class


class pollsmodule(commands.Cog, name="PollsModule", description="poll"):
    def __init__(self, bot):
        self.bot = bot

    # *********************************************************************************************************************
    # bot command to make a poll in chat
    # *********************************************************************************************************************
    @commands.command(name='giveaway', aliases=['createpoll', 'makepoll', 'polls', '💈'],
                      help='💈 Make a poll! [Max options: 9, Questions and Options with spaces need quotes ""]')
    # only specific roles can use this command
    @commands.has_role(role_specific_command_name)
    async def create_giveaway(self, ctx, question: Optional[str], *options):
        print("")

    # @commands.command(name="giveaway")
	# async def create_giveaway(self, ctx, mins: int, *, description: str):
	# 	embed = Embed(title="Giveaway",
	# 				  description=description,
	# 				  colour=ctx.author.colour,
	# 				  timestamp=datetime.utcnow())

	# 	fields = [("End time", f"{datetime.utcnow()+timedelta(seconds=mins*60)} UTC", False)]

	# 	for name, value, inline in fields:
	# 		embed.add_field(name=name, value=value, inline=inline)

	# 	message = await ctx.send(embed=embed)
	# 	await message.add_reaction("✅")

	# 	self.giveaways.append((message.channel.id, message.id))

	# 	self.bot.scheduler.add_job(self.complete_giveaway, "date", run_date=datetime.now()+timedelta(seconds=mins),
	# 							   args=[message.channel.id, message.id])

	# async def complete_poll(self, channel_id, message_id):
	# 	message = await self.bot.get_channel(channel_id).fetch_message(message_id)

	# 	most_voted = max(message.reactions, key=lambda r: r.count)

	# 	await message.channel.send(f"The results are in and option {most_voted.emoji} was the most popular with {most_voted.count-1:,} votes!")
	# 	self.polls.remove((message.channel.id, message.id))

	# async def complete_giveaway(self, channel_id, message_id):
	# 	message = await self.bot.get_channel(channel_id).fetch_message(message_id)

	# 	if len((entrants := [u for u in await message.reactions[0].users().flatten() if not u.bot])) > 0:
	# 		winner = choice(entrants)
	# 		await message.channel.send(f"Congratulations {winner.mention} - you won the giveaway!")
	# 		self.giveaways.remove((message.channel.id, message.id))

	# 	else:
	# 		await message.channel.send("Giveaway ended - no one entered!")
	# 		self.giveaways.remove((message.channel.id, message.id))

	# @Cog.listener()
	# async def on_raw_reaction_add(self, payload):
		# if self.bot.ready and payload.message_id == self.reaction_message.id:
		# 	current_colours = filter(lambda r: r in self.colours.values(), payload.member.roles)
		# 	await payload.member.remove_roles(*current_colours, reason="Colour role reaction.")
		# 	await payload.member.add_roles(self.colours[payload.emoji.name], reason="Colour role reaction.")
		# 	await self.reaction_message.remove_reaction(payload.emoji, payload.member)

		# elif payload.message_id in (poll[1] for poll in self.polls):
		# 	message = await self.bot.get_channel(payload.channel_id).fetch_message(payload.message_id)

		# 	for reaction in message.reactions:
		# 		if (not payload.member.bot
		# 			and payload.member in await reaction.users().flatten()
		# 			and reaction.emoji != payload.emoji.name):
		# 			await message.remove_reaction(reaction.emoji, payload.member)

		# elif payload.emoji.name == "⭐":
		# 	message = await self.bot.get_channel(payload.channel_id).fetch_message(payload.message_id)

		# 	if not message.author.bot and payload.member.id != message.author.id:
		# 		msg_id, stars = db.record("SELECT StarMessageID, Stars FROM starboard WHERE RootMessageID = ?",
		# 								  message.id) or (None, 0)

		# 		embed = Embed(title="Starred message",
		# 					  colour=message.author.colour,
		# 					  timestamp=datetime.utcnow())

		# 		fields = [("Author", message.author.mention, False),
		# 				  ("Content", message.content or "See attachment", False),
		# 				  ("Stars", stars+1, False)]

		# 		for name, value, inline in fields:
		# 			embed.add_field(name=name, value=value, inline=inline)

		# 		if len(message.attachments):
		# 			embed.set_image(url=message.attachments[0].url)

		# 		if not stars:
		# 			star_message = await self.starboard_channel.send(embed=embed)
		# 			db.execute("INSERT INTO starboard (RootMessageID, StarMessageID) VALUES (?, ?)",
		# 					   message.id, star_message.id)

		# 		else:
		# 			star_message = await self.starboard_channel.fetch_message(msg_id)
		# 			await star_message.edit(embed=embed)
		# 			db.execute("UPDATE starboard SET Stars = Stars + 1 WHERE RootMessageID = ?", message.id)

		# 	else:
		# 		await message.remove_reaction(payload.emoji, payload.member)


def setup(bot):
    bot.add_cog(pollsmodule(bot))
