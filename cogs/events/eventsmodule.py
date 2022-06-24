# *********************************************************************************************************************
# eventsmodule.py
# - giveaway command (wip)
# - polls command
# *********************************************************************************************************************

import os
import discord
import cogs.helper.constants.emoji_constants as emoji_constants

from discord.ext import commands
from discord import Embed
from typing import Optional

# role specific names
role_specific_command_name = 'Bot Commander'
admin_specific_command_name = 'Bot Admin'

# eventsmodule class


class eventsmodule(commands.Cog, name="EventsModule", description="polls"):
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


def setup(bot):
    bot.add_cog(eventsmodule(bot))
