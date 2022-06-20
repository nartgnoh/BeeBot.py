# *********************************************************************************************************************
# lolinfomodule.py
# - champ_lookup command
# - champ_skills command
# *********************************************************************************************************************

import os
import discord
import random
import requests
import cogs.helper.constants.lol_constants as lol_constants
import cogs.helper.api.league_of_legends_api as lolapi

from discord.ext import commands
from discord import Embed
from typing import Optional


# role specific names
role_specific_command_name = 'Bot Commander'
admin_specific_command_name = 'Bot Admin'

# lolinfomodule class


class lolinfomodule(commands.Cog, name="LoLInfoModule", description="champlookup, champskills"):
    def __init__(self, bot):
        self.bot = bot

    # *********************************************************************************************************************
    # bot command to lookup basic league of legends champion info
    # *********************************************************************************************************************
    @commands.command(name='champlookup', aliases=['champ', 'lolchamp', 'champlol', 'lookupchamp', '🔍'],
                      help='🔍 Quick lookup for lol champ information. [Auto: random champ]')
    # only specific roles can use this command
    @commands.has_role(role_specific_command_name)
    async def champ_lookup(self, ctx, *, lol_champion: Optional[str]):
        # get current lol version for region
        champions_version = lolapi.get_version()['n']['champion']
        champ_list = lolapi.get_champion_list(champions_version)['data']
        if lol_champion == None:
            lol_champion = random.choice(list(champ_list))
        else:
            # format string
            lol_champion = lol_champion.replace(
                "'", '').lower().title().replace(' ', '').strip('"')
        if lol_champion not in champ_list:
            await ctx.send("Sorry! An error has occurred! :cry: Check your spelling and try again! :slight_smile:")
        else:
            # API champion info
            champion_info = champ_list[lol_champion]
            champ_url = champion_info['name'].replace(
                "'", '-').replace(" ", '-').lower()
            # *********
            # | embed |
            # *********
            embed = Embed(title=champion_info['name'],
                          description=champion_info['title'],
                          colour=discord.Colour.random(),
                          url=f"https://www.leagueoflegends.com/en-us/champions/{champ_url}/")
            # embed thumbnail
            thumb_url = f'http://ddragon.leagueoflegends.com/cdn/{champions_version}/img/champion/{lol_champion}.png'
            embed.set_thumbnail(url=thumb_url)
            # add a new field to the embed
            embed.add_field(name=f'Tags:', value=', '.join(
                champion_info['tags']), inline=False)
            aff = champion_info['info']
            embed.add_field(
                name=f'Affinity:', value=f"| AD: {aff['attack']} | AP: {aff['magic']} | DEF: {aff['defense']} |", inline=False)
            await ctx.send(embed=embed)

    # *********************************************************************************************************************
    # bot command lookup abilities of league of legends champion
    # *********************************************************************************************************************
    @commands.command(name='champskills', aliases=['abilitychamp', 'champability', 'champabilities', 'abilitieschamp', 'schamp', 'champskill', '💥'],
                      help='💥 Full lookup for lol champ information. [Auto: random champ]')
    # only specific roles can use this command
    @commands.has_role(role_specific_command_name)
    async def champ_skill(self, ctx, *, lol_champion: Optional[str]):
        # get current lol version for region
        champions_version = lolapi.get_version()['n']['champion']
        champ_list = lolapi.get_champion_list(champions_version)['data']
        if lol_champion == None:
            lol_champion = random.choice(list(champ_list))
        else:
            # format string
            lol_champion = lol_champion.replace(
                "'", '').lower().title().replace(' ', '').strip('"')
        if lol_champion not in champ_list:
            await ctx.send("Sorry! An error has occurred! :cry: Check your spelling and try again! :slight_smile:")
        else:
            # API full champion info
            response = requests.get(
                f'http://ddragon.leagueoflegends.com/cdn/{champions_version}/data/en_US/champion/{lol_champion}.json')
            champion_info = response.json()['data'][lol_champion]
            champ_url = champion_info['name'].replace(
                "'", '-').replace(" ", '-').lower()
            # *********
            # | embed |
            # *********
            embed = Embed(title=champion_info['name'],
                          description=champion_info['title'],
                          colour=discord.Colour.random(),
                          url=f"https://www.leagueoflegends.com/en-us/champions/{champ_url}/")
            # embed image
            img_url = f'http://ddragon.leagueoflegends.com/cdn/img/champion/splash/{lol_champion}_0.jpg'
            embed.set_image(url=img_url)
            # embed fields
            embed.add_field(name=f"Passive: {champion_info['passive']['name']}",
                            value=f"Description: {champion_info['passive']['description']}", inline=False)
            spells = champion_info['spells']
            for (spell, game_key) in zip(spells, lol_constants.lol_keys()):
                embed.add_field(name=f"{game_key}: {spell['name']}",
                                value=f"Cooldown: {spell['cooldownBurn']}\nCost: {spell['costBurn']}\nRange: {spell['rangeBurn']}\nDescription: {spell['description']}",
                                inline=False)
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(lolinfomodule(bot))
