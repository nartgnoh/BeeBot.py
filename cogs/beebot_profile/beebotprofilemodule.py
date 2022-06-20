# *********************************************************************************************************************
# beebotprofilemodule.py
# - timezone
# *********************************************************************************************************************

import os
from time import time
import discord
import cogs.helper.helper_functions.timezones as timezones
import cogs.helper.helper_functions.beebot_profiles as beebot_profiles

from discord.ext import commands
from discord import Embed
from typing import Optional

# role specific names
role_specific_command_name = 'Bot Commander'
admin_specific_command_name = 'Bot Admin'

# beebotprofilemodule class


class beebotprofilemodule(commands.Cog, name="BeeBotProfileModule", description="timezone"):
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
        elif timezone not in timezones.list_all_timezones():
            await ctx.send("Sorry! You need to add a valid timezone! :open_mouth:")
        else:
            profile = str(ctx.message.author)
            beebot_profiles_data = beebot_profiles.get_beebot_profiles_json()
            beebot_profiles_data = beebot_profiles.beebot_profile_exists(
                beebot_profiles_data, profile)
            beebot_profiles_data[profile]["timezone"] = timezone
            beebot_profiles.set_beebot_profiles_json(beebot_profiles_data)
            await ctx.send("Your timezone has been updated! :white_check_mark:")


def setup(bot):
    bot.add_cog(beebotprofilemodule(bot))
