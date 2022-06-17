# *********************************************************************************************************************
# lolprofile.py
# - lolprofile command
# *********************************************************************************************************************

import os
import discord
import random
import json
import requests

from discord.ext import commands
from discord import Embed
from typing import Optional
from dotenv import load_dotenv
from riotwatcher import LolWatcher, ApiError

# get riot_lol_key from .env file
load_dotenv()
LOL_KEY = os.getenv('RIOT_LOL_KEY')
lol_watcher = LolWatcher(LOL_KEY)
default_region = 'na1'

# get current directory
current_directory = os.path.dirname(os.path.realpath(__file__))
# role specific names
role_specific_command_name = 'Bot Commander'
owner_specific_command_name = 'Server Owner'

# lolprofile class
class lolprofile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    # *********************************************************************************************************************
    # bot command to show the profile of a given summoner name (shows mastery, etc)
    # *********************************************************************************************************************
    @commands.command(name='lolprofile', aliases=['profilelol'], 
        help='👤 Showcase a summoner\'s league of legends profile. ')
    # only specific roles can use this command
    @commands.has_role(owner_specific_command_name)
    async def lol_profile(self, ctx, summoner_name: str, region: Optional[str]):
        if region == None:
            region = default_region

        else:
            await ctx.send("Sorry! An error has occurred! :cry: Check your spelling and try again! :slight_smile:")

def setup(bot):
    bot.add_cog(lolprofile(bot))