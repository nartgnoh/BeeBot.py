# *********************************************************************************************************************
# lolteamcomp.py
# - lol_balance command
# *********************************************************************************************************************

from ftplib import all_errors
import os
from pydoc import describe
import discord
import random
import json
import requests

from discord.ext import commands
from discord import Embed
from typing import Optional
from dotenv import load_dotenv
from riotwatcher import LolWatcher, ApiError
from collections import Counter

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

# lolteamcomp class
class lolteamcomp(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    # *********************************************************************************************************************
    # bot command to balance a league of legends team comp
    # *********************************************************************************************************************
    @commands.command(name='lolbalance', aliases=['balancelol', 'lolteamcomp', 'teamcomplol', 'lolteam', 'teamlol', '⚖️'], 
        help='⚖️ Help balance a lol teamcomp! [Put champions with spaces in quotes ""]')
    # only specific roles can use this command
    @commands.has_role(owner_specific_command_name)
    async def lol_balance(self, ctx, *lol_champions):
        if not lol_champions:
            await ctx.send("Sorry! You forgot to add champions! :slight_smile:")
        else:
            # get current lol version for region
            versions = lol_watcher.data_dragon.versions_for_region(default_region)
            champions_version = versions['n']['champion']
            champ_list = lol_watcher.data_dragon.champions(champions_version)['data']

            check = True
            # iterate through champion tags and info (affinity)
            tags_list = []
            affinity = {'AD': 0, 'AP': 0, 'DEF': 0}
            for champion in lol_champions:
                # format string
                champion = champion.lower().title().replace(' ', '')
                if champion not in champ_list:
                    check = False
                else:
                    # tags
                    tags = champ_list[champion]['tags']
                    for tag in tags:
                        tags_list.append(tag)
                    # info (affinity)
                    aff = champ_list[champion]['info']
                    ad = affinity['AD'] + aff['attack']
                    ap = affinity['AP'] + aff['magic']
                    de = affinity['DEF'] + aff['defense']
                    affinity.update({'AD': ad, 'AP': ap, 'DEF': de})

            if check:
                all_tags = ['Fighter', 'Tank', 'Mage', 'Assassin', 'Marksman', 'Support']
                # drop duplicates in list
                new_tags_list = list(dict.fromkeys(tags_list))

                # all_tags - new_tags_list
                missing_tags = [tag for tag in all_tags if tag not in new_tags_list]
                if not missing_tags:
                    missing_tags = 'Congrats! You covered all of the available tags! :tada:'
                else:
                    missing_tags = [s + 's' for s in missing_tags]
                    missing_tags = f"You team is missing some; \n***{', '.join(missing_tags)}***"
                # most common tag
                most_common_tag = max(tags_list, key = tags_list.count)
                # highest affinity
                highest_aff = max(affinity, key=affinity.get)
                # champions with useful tags
                available_champs = []
                for champion in champ_list:
                    if all(i in missing_tags for i in champ_list[champion]['tags']):
                        available_champs.append(champ_list[champion]['name'])
                if len(available_champs) >= 10:
                    available_champs = random.sample(available_champs, 10)

                # set initals to embed
                embed = Embed(title="Team Comp Balance!",
                            description="Check if your team is well balanced! :D",
                            colour=ctx.author.colour)
                # set image to embed
                file = discord.File(f'resource_files/image_files/thumbnails/lolbalance_thumb.png', filename="image.png")
                embed.set_thumbnail(url='attachment://image.png')
                # add a new field to the embed
                # set variables for fields to embed
                fields = [(f"Highest Affinity:", f"***{highest_aff}***", True),
                        (f"Most Common Tag:", f"***{most_common_tag}***", True),
                        ("Missing Tags:", missing_tags, False),
                        ("Available Champions:", f"Try adding these champions to your comp to round it out! c:\n***{', '.join(available_champs)}***", False)]
                for name, value, inline in fields:
                    embed.add_field(name=name, value=value, inline=inline)

                await ctx.send(file=file, embed=embed)
            else:
                await ctx.send("Sorry! An error has occurred! :cry: Check your spelling and try again!\n" +
                    "Don't forget to put champions with spaces in quotes \"\"! (ex; \"Miss Fortune\") :slight_smile:")        

def setup(bot):
    bot.add_cog(lolteamcomp(bot))