# lolclash.py

import os
import discord
import random

from discord.ext import commands
from typing import Optional

# get current directory
current_directory = os.path.dirname(os.path.realpath(__file__))
# role specific names
role_specific_command_name = 'Bot Commander'
owner_specific_command_name = 'Server Owner'

# lolclash class
class lolclash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    # *********************************************************************************************************************
    # bot command template
    # *********************************************************************************************************************
    @commands.command(name='command_name', aliases=['add_aliases'], help='~ Add description')
    # OPTIONAL: only specific roles can use this command
    @commands.has_role(owner_specific_command_name)
    async def command_name(self, ctx):
        # send message in discord chat
        await ctx.send('Send message in chat!')

def setup(bot):
    bot.add_cog(lolclash(bot))