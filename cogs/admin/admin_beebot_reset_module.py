# *********************************************************************************************************************
# admin_beebot_reset_module.py
# - admin_beebot_reset_all_events command
# - admin_beebot_reset_all_urls command (wip)
# - admin_beebot_reset_all_beebot_profiles command
# - ADMIN_BEEBOT_RESET_ALL_BEEBOT_FILES command (wip)
# *********************************************************************************************************************

import os
import discord
import cogs.helper.helper_functions.events as events
import cogs.helper.helper_functions.beebot_profiles as beebot_profiles

from discord.ext import commands
from discord import Embed
from typing import Optional
from datetime import datetime

# role specific names
role_specific_command_name = 'Bot Commander'
admin_specific_command_name = 'Bot Admin'

# admin_beebot_reset_module class


class admin_beebot_reset_module(commands.Cog, name="Admin_BeeBot_Reset_Module", description="Type \"BB help Admin_BeeBot_Reset_Module\" for options"):
    def __init__(self, bot):
        self.bot = bot

    # *********************************************************************************************************************
    # bot command admin beebot reset events
    # *********************************************************************************************************************
    @commands.command(name='admin_beebot_reset_all_events', help='🛡️ Reset BeeBot events file. [Admin Specific]')
    # only specific roles can use this command
    @commands.has_role(admin_specific_command_name)
    async def admin_beebot_reset_all_events(self, ctx):
        events.set_events_json({})
        await ctx.send('Reset BeeBot events file.')

    # # *********************************************************************************************************************
    # # bot command admin beebot reset urls
    # # *********************************************************************************************************************

    # *********************************************************************************************************************
    # bot command admin beebot reset beebot profiles
    # *********************************************************************************************************************
    @commands.command(name='admin_beebot_reset_all_beebot_profiles', help='🛡️ Reset BeeBot profiles file. [Admin Specific]')
    # only specific roles can use this command
    @commands.has_role(admin_specific_command_name)
    async def admin_beebot_reset_all_beebot_profiles(self, ctx):
        beebot_profiles.set_beebot_profiles_json({})
        await ctx.send('Reset BeeBot profiles file.')

    # # *********************************************************************************************************************
    # # bot command admin beebot reset ALL BEEBOT FILES
    # # *********************************************************************************************************************
    # @commands.command(name='(CAUTION)ADMIN_BEEBOT_RESET_ALL_BEEBOT_FILES', help='🛡️ Reset BeeBot ALL BEEBOT FILES. [Admin Specific]')
    # # only specific roles can use this command
    # @commands.has_role(admin_specific_command_name)
    # async def ADMIN_BEEBOT_RESET_ALL_BEEBOT_FILES(self, ctx):
    #     await ctx.send('BB admin_beebot_reset_all_beebot_profiles')
    #     await ctx.send('BB admin_beebot_reset_all_events')


def setup(bot):
    bot.add_cog(admin_beebot_reset_module(bot))
