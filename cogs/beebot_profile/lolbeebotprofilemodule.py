# *********************************************************************************************************************
# lolbeebotprofilemodule.py
# - lol_roles
# *********************************************************************************************************************

import os
import discord
import json
import cogs.constants.lolconstants as lolconstants

from discord.ext import commands
from discord import Embed
from typing import Optional

# get current directory
current_directory = os.path.dirname(os.path.realpath(__file__))
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
                      f"[Valid Roles: {', '.join(lolconstants.lol_roles())}]")
    # only specific roles can use this command
    @commands.has_role(role_specific_command_name)
    async def lol_roles(self, ctx, *roles):
        roles = list(roles)
        if not roles:
            await ctx.send("Sorry! You need to add role(s)! :open_mouth:")
        else:
            roles_list = []
            for role in roles:
                if role.title() in lolconstants.lol_roles():
                    roles_list.append(role.lower())
            roles_list = list(dict.fromkeys(roles_list))
            # read beebot_profiles.json file
            beebot_profiles_json = "/".join(list(current_directory.split('/')
                                                 [0:-2])) + '/resource_files/json_files/beebot_profiles.json'
            with open(beebot_profiles_json) as f:
                beebot_profiles_data = json.load(f)
            # add profile's roles
            profile = str(ctx.message.author)
            if profile not in beebot_profiles_data:
                beebot_profiles_data[profile] = {}
            if "league_of_legends" not in beebot_profiles_data[profile]:
                beebot_profiles_data[profile]["league_of_legends"] = {
                }
            beebot_profiles_data[profile]["league_of_legends"][
                'preferred_role(s)'] = roles_list
            # write to beebot_profiles.json file
            with open(beebot_profiles_json, 'w') as outfile:
                json.dump(beebot_profiles_data, outfile)
            await ctx.send("Your role(s) have been updated! :white_check_mark:")


def setup(bot):
    bot.add_cog(lolbeebotprofilemodule(bot))
