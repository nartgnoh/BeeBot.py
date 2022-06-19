# *********************************************************************************************************************
# lolteamsmodule.py
# - lol_balance command
# *********************************************************************************************************************

from ftplib import all_errors
import os
from pydoc import describe
import discord
import random
import cogs.constants.lolconstants as lolconstants

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
owner_specific_command_name = 'Bot Admin'

# lolteamsmodule class


class lolteamsmodule(commands.Cog, name="LoLTeamsModule", description="lolbalance"):
    def __init__(self, bot):
        self.bot = bot

    # *********************************************************************************************************************
    # bot command to balance a league of legends team comp
    # *********************************************************************************************************************
    @commands.command(name='lolbalance', aliases=['balancelol', 'lolteamcomp', 'teamcomplol', 'lolteam', 'teamlol', 'lolteams', 'teamslol', '⚖️'],
                      help='⚖️ Help balance a lol teamcomp! [Champions with spaces need quotes ""]')
    # only specific roles can use this command
    @commands.has_role(role_specific_command_name)
    async def lol_balance(self, ctx, *lol_champions):
        if not lol_champions:
            await ctx.send("Sorry! You forgot to add champions! :slight_smile:")
        else:
            # get current lol version for region
            versions = lol_watcher.data_dragon.versions_for_region(
                default_region)
            champions_version = versions['n']['champion']
            champ_list = lol_watcher.data_dragon.champions(champions_version)[
                'data']
            check = True
            # iterate through champion tags and info (affinity)
            tags_list = []
            affinity = {'AD': 0, 'AP': 0, 'DEF': 0}
            for champion in lol_champions:
                # format string
                champion = champion.replace("'", '').lower(
                ).title().replace(' ', '').strip('"')
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

            if not check:
                await ctx.send("Sorry! An error has occurred! :cry: "
                               "Check your spelling and try again!\n"
                               "Don't forget to put champions with spaces in quotes \"\"! "
                               "(ex; \"Miss Fortune\") :slight_smile:")
            else:
                all_tags = lolconstants.lol_tags()
                # drop duplicates in list
                new_tags_list = list(dict.fromkeys(tags_list))
                # all_tags - new_tags_list
                missing_tags = [
                    tag for tag in all_tags if tag not in new_tags_list]
                # most common tag
                most_common_tag = max(tags_list, key=tags_list.count)
                # highest affinity
                highest_aff = max(affinity, key=affinity.get)
                # champions with useful tags
                available_champs = []
                for champion in champ_list:
                    if any(i in missing_tags for i in champ_list[champion]['tags']):
                        available_champs.append(champ_list[champion]['name'])
                if len(available_champs) >= 10:
                    available_champs = random.sample(available_champs, 10)
                missing_txt = ''
                available_txt = ''
                if not missing_tags:
                    missing_txt = '-'
                    available_txt = '-'
                else:
                    missing_tags = [s + 's' for s in missing_tags]
                    missing_txt = f"You team is missing some; \n***{', '.join(missing_tags)}***"
                    available_txt = f"Try adding these champions to your comp to round it out! c:\n***{', '.join(available_champs)}***"
                # *********
                # | embed |
                # *********
                embed = Embed(title="Team Comp Balance!",
                              description="Check if your team is well balanced! :D",
                              colour=ctx.author.colour)
                # embed thumbnail
                file = discord.File(
                    f'resource_files/image_files/thumbnails/lolbalance_thumb.png', filename="image.png")
                embed.set_thumbnail(url='attachment://image.png')
                # embed fields
                fields = [(f"Highest Affinity:", f"***{highest_aff}***", True),
                          (f"Most Common Tag:",
                           f"***{most_common_tag}***", True),
                          ("Missing Tags:", missing_txt, False),
                          ("Available Champions:", available_txt, False)]
                for name, value, inline in fields:
                    embed.add_field(name=name, value=value, inline=inline)
                if not missing_tags:
                    embed.add_field(name=f':tada: Congrats! Your team covers all of the available tags! :tada:',
                                    value='Now you\'re ready to hit the rift!', inline=False)
                await ctx.send(file=file, embed=embed)


def setup(bot):
    bot.add_cog(lolteamsmodule(bot))
