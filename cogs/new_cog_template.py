# *********************************************************************************************************************
# new_cog_template.py
# - 
# *********************************************************************************************************************

# **********************************************************************************
# New Cog Steps:
# 1. Replace all occurences of "new_cog_template" with new "cog_name"
# 2. Add new "cog_name" to existing bee_bot.py file in the [all_extensions] list 
#       (for cogs inside directories, add cogs.<directory>.<cog_name>)
# 3. Add new commands using the command template below
# **********************************************************************************

import os
import discord
import random

from discord.ext import commands
from discord import Embed
from typing import Optional

# get current directory
current_directory = os.path.dirname(os.path.realpath(__file__))
# role specific names
role_specific_command_name = 'Bot Commander'
owner_specific_command_name = 'Server Owner'

# new_cog_template class
class new_cog_template(commands.Cog):
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
    bot.add_cog(new_cog_template(bot))