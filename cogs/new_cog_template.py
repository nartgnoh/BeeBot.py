# *********************************************************************************************************************
# new_cog_template_module.py
# -
# *********************************************************************************************************************

# **********************************************************************************
# New Cog Steps:
# 1. Replace all occurences of "new_cog_template_module" with new "cog_name"
# 2. Add new "cog_name" to existing bee_bot.py file in the [all_extensions] list
#       (for cogs inside directories, add cogs.<directory>.<cog_name>)
# 3. Add new commands using the command template below
# **********************************************************************************

import os
import discord

from discord.ext import commands
from discord import Embed
from typing import Optional

# role specific names
role_specific_command_name = 'Bot Commander'
admin_specific_command_name = 'Bot Admin'

# new_cog_template_module class


class new_cog_template_module(commands.Cog, name="new_cog_template_module", description=""):
    def __init__(self, bot):
        self.bot = bot

    # *********************************************************************************************************************
    # bot command template
    # *********************************************************************************************************************
    @commands.command(name='command_name', aliases=['add_aliases'], help='~ Add description')
    # only specific roles can use this command
    # @commands.has_role(admin_specific_command_name)
    async def command_name(self, ctx):
        # # *********
        # # | embed |
        # # *********
        # embed = Embed(title="Title",
        #         description="description",
        #         colour=ctx.author.colour)
        # # embed fields
        # embed.add_field(name="name", value="value", inline=False)

        # # *************
        # # | reactions |
        # # *************
        # msg = await ctx.send('Send message in chat!')

        # send message in discord chat
        await ctx.send('Send message in chat!')


def setup(bot):
    bot.add_cog(new_cog_template_module(bot))
