# *********************************************************************************************************************
# giveawaymodule.py
# - giveaway command
# *********************************************************************************************************************

import os
import discord
import warnings
import cogs.helper.constants.emoji_constants as emoji_constants
import cogs.helper.helper_functions.emojis as emojis

from discord.ext import commands
from discord.ext.commands import Cog
from discord import Embed
from typing import Optional
from datetime import datetime, timedelta

warnings.filterwarnings("error")

# role specific names
role_specific_command_name = 'Bot Commander'
admin_specific_command_name = 'Bot Admin'

# giveawaymodule class


class giveawaymodule(commands.Cog, name="GiveawayModule", description="giveaway"):
    def __init__(self, bot):
        self.bot = bot

    # *********************************************************************************************************************
    # bot command to make a giveaway in chat
    # *********************************************************************************************************************
    @commands.command(name='giveaway', aliases=['creategiveaway', 'makegiveaway', '🎁'],
                      help='🎁 Make a giveaway! [Titles with spaces need quotes ""]')
    # only specific roles can use this command
    @commands.has_role(role_specific_command_name)
    async def create_giveaway(self, ctx, title: Optional[str], reaction: Optional[str], *, description: Optional[str]):
        if title == None:
            return await ctx.send("Sorry! You forgot to add inputs! :open_mouth: Please provide some! :slight_smile:")
        if reaction == None or not emojis.check_emoji(reaction):
            return await ctx.send("Sorry! You have an invalid emoji! :cry: Please try again! :smile:")

        # *********
        # | embed |
        # *********
        embed = Embed(title=f"{ctx.author.display_name}'s __{title}__ Giveaway!",
                      description=f"React with {reaction} to join the giveaway!",
                      colour=ctx.author.colour)
        # embed fields
        embed.add_field(name="Giveaway Description:",
                        value=description, inline=False)
        # embed footer
        embed.set_footer(
            text=f"{reaction} Type \"BB endgiveaway {title}\" to end the giveaway!")
        await ctx.send(embed=embed)

        # if question == None:
        # embed = Embed(title="Giveaway",
        # 			  description=description,
        # 			  colour=ctx.author.colour,
        # 			  timestamp=datetime.utcnow())

        # fields = [
        #     ("End time", f"{datetime.utcnow()+timedelta(seconds=mins*60)} UTC", False)]

        # for name, value, inline in fields:
        # 	embed.add_field(name=name, value=value, inline=inline)

        # message = await ctx.send(embed=embed)
        # await message.add_reaction("✅")

        # self.giveaways.append((message.channel.id, message.id))

        # self.bot.scheduler.add_job(self.complete_giveaway, "date", run_date=datetime.now()+timedelta(seconds=mins),
        # 						   args=[message.channel.id, message.id])

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

        # elif payload.message_id in (poll[1] for poll in self.giveaway):
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
    bot.add_cog(giveawaymodule(bot))
