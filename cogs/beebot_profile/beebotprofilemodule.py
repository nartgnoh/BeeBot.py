# *********************************************************************************************************************
# beebotprofilemodule.py
# - timezone
# *********************************************************************************************************************

import os
from time import time
import discord
import json
import cogs.functions.timezone_functions as timezone_functions

from discord.ext import commands
from discord import Embed
from typing import Optional

# get current directory
current_directory = os.path.dirname(os.path.realpath(__file__))
# role specific names
role_specific_command_name = 'Bot Commander'
admin_specific_command_name = 'Bot Admin'

# beebotprofilemodule class


class beebotprofilemodule(commands.Cog, name="BeeBotProfileModule", description="Setup your BeeBot profile!"):
    def __init__(self, bot):
        self.bot = bot

    # *********************************************************************************************************************
    # bot command setup local timezone of user
    # *********************************************************************************************************************
    @commands.command(name='timezone', aliases=['tz', 'timezones', 'bbtz', 'bbtimezone', 'bbtimezones', '🌐'],
                      help="🌐 Set your timezone to your BeeBot profile!\n\n"
                      f"[Valid timezones can be found @ https://gist.github.com/heyalexej/8bf688fd67d7199be4a1682b3eec7568 ]")
    # only specific roles can use this command
    @commands.has_role(role_specific_command_name)
    async def timezone(self, ctx, timezone: Optional[str]):
        if timezone == None:
            await ctx.send("Sorry! You need to add your timezone! :open_mouth:")
        elif timezone not in timezone_functions.list_all_timezones():
            await ctx.send("Sorry! You need to add a valid timezone! :open_mouth:")
        else:
            # read beebot_profiles.json file
            beebot_profiles_json = "/".join(list(current_directory.split('/')
                                                 [0:-2])) + '/resource_files/json_files/beebot_profiles.json'
            with open(beebot_profiles_json) as f:
                beebot_profiles_data = json.load(f)
            # add profile's timezone
            profile = str(ctx.message.author)
            if profile not in beebot_profiles_data:
                beebot_profiles_data[profile] = {}
            beebot_profiles_data[profile]["timezone"] = timezone
            # write to beebot_profiles.json file
            with open(beebot_profiles_json, 'w') as outfile:
                json.dump(beebot_profiles_data, outfile)
            await ctx.send("Your timezone has been updated! :white_check_mark:")


def setup(bot):
    bot.add_cog(beebotprofilemodule(bot))