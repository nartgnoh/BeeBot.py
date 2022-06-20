# *********************************************************************************************************************
# viewmusicmodule.py
# - (wip)
# *********************************************************************************************************************

import os
import discord
import random

from discord.ext import commands
from discord import Embed
from typing import Optional

# role specific names
role_specific_command_name = 'Bot Commander'
admin_specific_command_name = 'Bot Admin'

# viewmusicmodule class


class viewmusicmodule(commands.Cog, name="ViewMusicModule", description=""):
    def __init__(self, bot):
        self.bot = bot

    # *********************************************************************************************************************
    # bot command template
    # *********************************************************************************************************************
    @commands.command(name='command_name', aliases=['add_aliases'], help='~ Add description')
    # only specific roles can use this command
    # @commands.has_role(admin_specific_command_name)
    async def command_name(self, ctx):
        # send message in discord chat
        await ctx.send('Send message in chat!')


def setup(bot):
    bot.add_cog(viewmusicmodule(bot))
