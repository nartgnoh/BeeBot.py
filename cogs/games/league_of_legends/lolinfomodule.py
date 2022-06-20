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
import cogs.helper.api.league_of_legends_api as lol_api

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
                      help='🔍 Quick lookup for lol champion. [Auto: random champ]')
    # only specific roles can use this command
    @commands.has_role(role_specific_command_name)
    async def champ_lookup(self, ctx, *, lol_champion: Optional[str]):
        # get current lol version for region
        champions_version = lol_api.get_version()['n']['champion']
        champ_list = lol_api.get_champion_list(champions_version)['data']
        if lol_champion == None:
            lol_champion = random.choice(list(champ_list))
        else:
            lol_champion = lol_api.champion_string_formatting(lol_champion)
        if lol_champion not in champ_list:
            await ctx.send("Sorry! An error has occurred! :cry: Check your spelling and try again! :slight_smile:")
        else:
            # API champion info
            champion_info = champ_list[lol_champion]
            # *********
            # | embed |
            # *********
            embed = Embed(title=champion_info['name'],
                          description=champion_info['title'],
                          colour=discord.Colour.random(),
                          url=lol_api.champion_url_by_name(champion_info['name']))
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
    @commands.command(name='champskills', aliases=['abilitychamp', 'champability', 'champabilities', 'abilitieschamp',
                                                   'schamp', 'champskill', 'skillschamp', '💥'],
                      help='💥 Full skills lookup for lol champion. [Auto: random champ]\n\n'
                      '[Add an "❌" reaction to delete]')
    # only specific roles can use this command
    @commands.has_role(role_specific_command_name)
    async def champ_skill(self, ctx, *, lol_champion: Optional[str]):
        # get current lol version for region
        champions_version = lol_api.get_version()['n']['champion']
        champ_list = lol_api.get_champion_list(champions_version)['data']
        if lol_champion == None:
            lol_champion = random.choice(list(champ_list))
        else:
            lol_champion = lol_api.champion_string_formatting(lol_champion)
        if lol_champion not in champ_list:
            await ctx.send("Sorry! An error has occurred! :cry: Check your spelling and try again! :slight_smile:")
        else:
            # API full champion info
            response = requests.get(
                f'http://ddragon.leagueoflegends.com/cdn/{champions_version}/data/en_US/champion/{lol_champion}.json')
            champion_info = response.json()['data'][lol_champion]
            # *********
            # | embed |
            # *********
            embed = Embed(title=champion_info['name'],
                          description=champion_info['title'],
                          colour=discord.Colour.random(),
                          url=lol_api.champion_url_by_name(champion_info['name']))
            # embed image
            img_url = f'http://ddragon.leagueoflegends.com/cdn/img/champion/splash/{lol_champion}_0.jpg'
            embed.set_image(url=img_url)
            # embed fields
            embed.add_field(name=f"Passive: {champion_info['passive']['name']}",
                            value=f"Description: {champion_info['passive']['description']}", inline=False)
            spells = champion_info['spells']
            for (spell, game_key) in zip(spells, lol_constants.lol_keys()):
                embed.add_field(name=f"{game_key}: {spell['name']}",
                                value=f"Cooldown: {spell['cooldownBurn']}\nCost: {spell['costBurn']}\n"
                                "Range: {spell['rangeBurn']}\nDescription: {spell['description']}",
                                inline=False)
            msg = await ctx.send(embed=embed)
            await msg.add_reaction("❌")


def setup(bot):
    bot.add_cog(lolinfomodule(bot))
