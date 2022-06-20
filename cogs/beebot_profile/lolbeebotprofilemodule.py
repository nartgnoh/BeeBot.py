# *********************************************************************************************************************
# lolbeebotprofilemodule.py
# - lol_roles
# *********************************************************************************************************************

import os
import discord
import cogs.helper.constants.lol_constants as lol_constants
import cogs.helper.helper_functions.beebot_profiles as beebot_profiles

from discord.ext import commands
from discord import Embed
from typing import Optional

# role specific names
role_specific_command_name = 'Bot Commander'
admin_specific_command_name = 'Bot Admin'

# lolbeebotprofilemodule class


class lolbeebotprofilemodule(commands.Cog, name="LoLBeeBotProfileModule", description="Setup your League of Legends BeeBot profile!"):
    def __init__(self, bot):
        self.bot = bot

    # *********************************************************************************************************************
    # bot command to set league of legends roles for beebot profile
    # *********************************************************************************************************************
    @commands.command(name='lolroles', aliases=['roleslol', 'lolrole', 'rolelol', '🤸'],
                      help="🤸 Set LoL preferred role(s) to your BeeBot profile!\n\n"
                      f"[Valid Roles: {', '.join(lol_constants.lol_roles())}]")
    # only specific roles can use this command
    @commands.has_role(role_specific_command_name)
    async def lol_roles(self, ctx, *roles):
        roles = list(roles)
        if not roles:
            await ctx.send("Sorry! You need to add role(s)! :open_mouth:")
        else:
            roles_list = []
            for role in roles:
                if role.title() in lol_constants.lol_roles():
                    roles_list.append(role.lower())
            roles_list = list(dict.fromkeys(roles_list))
            profile = str(ctx.message.author)
            beebot_profiles_data = beebot_profiles.get_beebot_profiles_json()
            beebot_profiles.beebot_profile_exists(
                beebot_profiles_data, profile)
            beebot_profiles.beebot_profile_key_exists(
                beebot_profiles_data, profile, "league_of_legends")
            beebot_profiles_data[profile]["league_of_legends"][
                'preferred_role(s)'] = roles_list
            beebot_profiles.set_beebot_profiles_json(beebot_profiles_data)
            await ctx.send("Your role(s) have been updated! :white_check_mark:")


def setup(bot):
    bot.add_cog(lolbeebotprofilemodule(bot))
