# *********************************************************************************************************************
# pollsmodule.py
# - poll command
# - giveaway command (wip)
# *********************************************************************************************************************

import os
import discord
import cogs.helper.constants.emoji_constants as emoji_constants

from discord.ext import commands
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
    @commands.command(name='poll', aliases=['createpoll', 'makepoll', 'polls', '💈'],
                      help='💈 Make a poll! [Max options: 9, Questions and Options with spaces need quotes ""]')
    # only specific roles can use this command
    @commands.has_role(role_specific_command_name)
    async def create_poll(self, ctx, question: Optional[str], *options):
        poll_hearts = emoji_constants.hearts()
        if question == None:
            await ctx.send("Please add a question and option(s)! :slight_smile:")
        else:
            if len(options) == 0:
                await ctx.send("Please add option(s)! :slight_smile:")
            elif len(options) > 9:
                await ctx.send("Sorry! You have too many options! :cry: Please try again! [Max options: 9]")
            else:
                # *********
                # | embed |
                # *********
                embed = Embed(title="Polls",
                              description=question,
                              colour=ctx.author.colour)
                # embed footer
                embed.set_footer(
                    text=f'Poll created by: {ctx.author.display_name}', icon_url=ctx.author.avatar_url)
                # embed fields
                fields = [("Options", "\n".join([f"{poll_hearts[idx]} {option}" for idx, option in enumerate(options)]), False),
                          ("Instructions", "React to cast a vote!", False)]
                for name, value, inline in fields:
                    embed.add_field(name=name, value=value, inline=inline)
                # *************
                # | reactions |
                # *************
                msg = await ctx.send(embed=embed)
                for emoji in poll_hearts[:len(options)]:
                    await msg.add_reaction(emoji)

    # # *********************************************************************************************************************
    # # bot command to make a poll in chat
    # # *********************************************************************************************************************
    # @commands.command(name='giveaway', aliases=['setgiveaway', 'giveawaysetup', 'polls', '💈'], help='🎁 Make a giveaway! [Put your question in quotes "", Max options: 9]')
    # # only specific roles can use this command
    # @commands.has_role(role_specific_command_name)
    # async def create_giveaway(self, ctx, mins: int, *, description: str):
    #     embed = Embed(title="Giveaway",
    #             description=description,
    #             colour=ctx.author.colour,
    #             timestamp=datetime.utcnow())

    #     fields = [("End time", f"{datetime.utcnow()+timedelta(seconds=mins*60)} UTC", False)]

        # 	for name, value, inline in fields:
        # 		embed.add_field(name=name, value=value, inline=inline)

        # 	message = await ctx.send(embed=embed)
    #     await message.add_reaction("✅")

    # self.giveaways.append((message.channel.id, message.id))

    # self.bot.scheduler.add_job(self.complete_giveaway, "date", run_date=datetime.now()+timedelta(seconds=mins),
    #                         args=[message.channel.id, message.id])

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


def setup(bot):
    bot.add_cog(pollsmodule(bot))
