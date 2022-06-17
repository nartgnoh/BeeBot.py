# poll.py

import os
import discord
import random

from discord.ext import commands
from discord import Embed
from typing import Optional
from datetime import datetime, timedelta

# get current directory
current_directory = os.path.dirname(os.path.realpath(__file__))
# role specific names
role_specific_command_name = 'Bot Commander'
owner_specific_command_name = 'Server Owner'

poll_hearts = ("❤️", "🧡", "💛", "💚", "💙", "💜", "🤎", "🖤", "🤍")

# poll class


class poll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    # *********************************************************************************************************************
    # bot command to make a poll in chat
    # *********************************************************************************************************************

    @commands.command(name='poll', aliases=['createpoll', 'makepoll', 'polls'], help='💈 Make a poll! [Put your question in quotes "", Max options: 9]')
    # only specific roles can use this command
    @commands.has_role(role_specific_command_name)
    async def command_name(self, ctx, question: str, *options):
        if len(options) == 0:
            await ctx.send("Please add some options! :slight_smile:")
        elif len(options) > 9:
            await ctx.send("Sorry, you have too many options! D: Please try again.")
        else:
            embed = Embed(title="Poll!",
                          description=question,
                          colour=ctx.author.colour)

            fields = [("Options", "\n".join([f"{poll_hearts[idx]} {option}" for idx, option in enumerate(options)]), False),
                         ("Instructions", "React to cast a vote!", False)]

            for name, options, instructions in fields:
                embed.add_field(name=name, options=options, instructions=instructions)

            msg = await ctx.send(embed=embed)

            for emoji in poll_hearts[:len(options)]:
                await msg.add_reaction(emoji)

def setup(bot):
    bot.add_cog(poll(bot))
