# *********************************************************************************************************************
# admin_beebot_reset_module.py
# - admin_beebot_reset_all_events command
# - admin_beebot_reset_all_urls command (wip)
# - admin_beebot_reset_all_beebot_profiles command
# - ADMIN_BEEBOT_RESET_ALL_BEEBOT_FILES command (wip)
# *********************************************************************************************************************

import os
import discord
import json

from discord.ext import commands
from discord import Embed
from typing import Optional
from datetime import datetime

# get current directory
current_directory = os.path.dirname(os.path.realpath(__file__))
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
        # read events.json file
        event_json = "/".join(list(current_directory.split('/')
                              [0:-2])) + '/resource_files/json_files/events.json'
        with open(event_json, 'w') as outfile:
            json.dump({}, outfile)
        await ctx.send('Reset BeeBot events file.')

    # # *********************************************************************************************************************
    # # bot command admin beebot reset urls
    # # *********************************************************************************************************************
    # @commands.command(name='admin_beebot_reset_all_urls', help='🛡️ Reset BeeBot urls file. [Admin Specific]')
    # # only specific roles can use this command
    # @commands.has_role(admin_specific_command_name)
    # async def admin_beebot_reset_all_events(self, ctx):
    #     # read events.json file
    #     event_json = "/".join(list(current_directory.split('/')
    #                           [0:-2])) + '/resource_files/json_files/events.json'
    #     with open(event_json, 'w') as outfile:
    #         json.dump({}, outfile)
    #     await ctx.send('Reset BeeBot event files.')

    # *********************************************************************************************************************
    # bot command admin beebot reset beebot profiles
    # *********************************************************************************************************************
    @commands.command(name='admin_beebot_reset_all_beebot_profiles', help='🛡️ Reset BeeBot profiles file. [Admin Specific]')
    # only specific roles can use this command
    @commands.has_role(admin_specific_command_name)
    async def admin_beebot_reset_all_beebot_profiles(self, ctx):
        # read beebot_profiles.json file
        beebot_profile_json = "/".join(list(current_directory.split('/')
                                            [0:-2])) + '/resource_files/json_files/beebot_profiles.json'
        with open(beebot_profile_json, 'w') as outfile:
            json.dump({}, outfile)
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
