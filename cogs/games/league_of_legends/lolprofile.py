# *********************************************************************************************************************
# lolprofile.py
# - lol_profile command
# - lol_rank command
# - lol_mastery command
# *********************************************************************************************************************

import os
import discord
import random
import json
import requests
import cogs.games.league_of_legends.lolconstants as lolconstants

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
    # bot command to show the full profile of a given summoner name (shows rank and mastery)
    # *********************************************************************************************************************
    @commands.command(name='lolprofile', aliases=['profilelol', 'lolp', 'plol', '👤'], 
        help='👤 Showcase a summoner\'s league of legends profile. [Put summoner names with spaces in quotes ""]')
    # only specific roles can use this command
    @commands.has_role(role_specific_command_name)
    async def lol_profile(self, ctx, summoner_name: str, region: Optional[str]):
        if region == None:
            region = default_region
        if region not in lolconstants.riot_regions():
            await ctx.send("Sorry! An error has occurred! :cry: Check that you have a valid region! :slight_smile:")
        else:
            # get current lol version for region
            versions = lol_watcher.data_dragon.versions_for_region(region)
            champions_version = versions['n']['champion']

            # get summoner info
            summoner = lol_watcher.summoner.by_name(region, summoner_name)
            # get summoner ranks
            ranks = lol_watcher.league.by_summoner(region, summoner['id'])
            # get total mastery
            total_mastery = lol_watcher.champion_mastery.scores_by_summoner(region, summoner['id'])
            # get top mastery
            top_mastery = lol_watcher.champion_mastery.by_summoner(region, summoner['id'])[0]
            # get top mastery champ
            champ_list = lol_watcher.data_dragon.champions(champions_version)['data']
            top_master_champ_info = ''
            for champion in champ_list:
                if top_mastery['championId'] == int(champ_list[champion]['key']):
                    top_master_champ_info = champion
                    break
            top_master_champ_info = champ_list[top_master_champ_info]

            # API image urls
            thumb_url = f"http://ddragon.leagueoflegends.com/cdn/{champions_version}/img/profileicon/{summoner['profileIconId']}.png"

            # set initals to embed
            embed = Embed(title=f"{summoner['name']}'s LOL Profile!",
                        description=f"Summoner Level: {summoner['summonerLevel']}",
                        colour=ctx.author.colour)
            # set image to embed
            embed.set_thumbnail(url=thumb_url)
            # add a new field to the embed
            if ranks:
                for rank in ranks:
                    embed.add_field(name=f"{rank['queueType']} Rank:".replace("_", " ").title(), 
                        value=f"{rank['tier'].title()} {rank['rank']} {rank['leaguePoints']}LP\n" + 
                        f"Wins: {rank['wins']} Losses: {rank['losses']}", inline=False)
                embed.add_field(name='\u200b',value='\u200b',inline=False)
            # set variables for fields to embed
            fields = [("Total Champion Mastery Score:", f"*{total_mastery}*", False),
                    ("Highest Mastery Champion:", f"*{top_master_champ_info['name']}*", False),
                    ("Mastery Level:", f"*{top_mastery['championLevel']}*", True),
                    ("Mastery Points:", f"*{top_mastery['championPoints']}*", True)]
            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)
            await ctx.send(embed=embed)

    # *********************************************************************************************************************
    # bot command to show the rank of a given summoner name
    # *********************************************************************************************************************
    @commands.command(name='lolrank', aliases=['ranklol', 'lolr', 'rlol', '🏆'], 
        help='🏆 Showcase a summoner\'s league of legends rank. [Put summoner names with spaces in quotes ""]')
    # only specific roles can use this command
    @commands.has_role(role_specific_command_name)
    async def lol_rank(self, ctx, summoner_name: str, region: Optional[str]):
        if region == None:
            region = default_region
        if region not in lolconstants.riot_regions():
            await ctx.send("Sorry! An error has occurred! :cry: Check that you have a valid region! :slight_smile:")
        else:
            # get current lol version for region
            versions = lol_watcher.data_dragon.versions_for_region(region)
            champions_version = versions['n']['champion']

            # get summoner info
            summoner = lol_watcher.summoner.by_name(region, summoner_name)
            # get summoner ranks
            ranks = lol_watcher.league.by_summoner(region, summoner['id'])

            # API image urls
            img_url = f"http://ddragon.leagueoflegends.com/cdn/{champions_version}/img/map/map11.png"
            thumb_url = f"http://ddragon.leagueoflegends.com/cdn/{champions_version}/img/profileicon/{summoner['profileIconId']}.png"

            # set initals to embed
            embed = Embed(title=f"{summoner['name']}'s LOL Rank!",
                        description=f"Summoner Level: {summoner['summonerLevel']}",
                        colour=ctx.author.colour)
            # set image to embed
            
            embed.set_thumbnail(url=thumb_url)
            # add a new field to the embed
            if ranks:
                riot_ranks = lolconstants.riot_ranks()
                total_rank = 0
                for rank in ranks:
                    embed.add_field(name=f"{rank['queueType']} Rank:".replace("_", " ").title(), 
                        value=f"{rank['tier'].title()} {rank['rank']} {rank['leaguePoints']}LP\n" + 
                        f"Wins: {rank['wins']} Losses: {rank['losses']}", inline=False)
                    # get average_rank
                    rank_key = [k for k,v in riot_ranks.items() if v == {'tier': rank['tier'], 'rank': rank['rank']}]
                    total_rank = total_rank + sum(rank_key)
                average_rank = round(total_rank/len(ranks), 0)
                final_rank = riot_ranks.get(int(average_rank))

                embed.add_field(name=f"Average Rank:", value=f"{final_rank['tier'].title()} {final_rank['rank']}",inline=False)
                file = discord.File(f"resource_files/image_files/riot_images/ranked_emblems/Emblem_{final_rank['tier'].title()}.png", 
                    filename="image.png")
                embed.set_image(url='attachment://image.png')
                await ctx.send(file=file, embed=embed)
            else:
                embed.add_field(name="This summoner has nothing for ranked this season.",value="Maybe it's time?... 👀",inline=False)
                embed.set_image(url=img_url)
                await ctx.send(embed=embed)
            

    # *********************************************************************************************************************
    # bot command to show the mastery of a given summoner name
    # *********************************************************************************************************************
    @commands.command(name='lolmastery', aliases=['masterylol', 'lolm', 'mlol', '🎓'], 
        help='🎓 Showcase a summoner\'s league of legends mastery. [Put summoner names with spaces in quotes ""]')
    # only specific roles can use this command
    @commands.has_role(role_specific_command_name)
    async def lol_mastery(self, ctx, summoner_name: str, region: Optional[str]):
        if region == None:
            region = default_region
        if region not in lolconstants.riot_regions():
            await ctx.send("Sorry! An error has occurred! :cry: Check that you have a valid region! :slight_smile:")
        else:
            # get current lol version for region
            versions = lol_watcher.data_dragon.versions_for_region(region)
            champions_version = versions['n']['champion']

            # get summoner info
            summoner = lol_watcher.summoner.by_name(region, summoner_name)
            # get total mastery
            total_mastery = lol_watcher.champion_mastery.scores_by_summoner(region, summoner['id'])
            # get top mastery
            top_mastery = lol_watcher.champion_mastery.by_summoner(region, summoner['id'])[0]
            # get top mastery champ
            champ_list = lol_watcher.data_dragon.champions(champions_version)['data']
            top_master_champ_info = ''
            for champion in champ_list:
                if top_mastery['championId'] == int(champ_list[champion]['key']):
                    top_master_champ_info = champion
                    break
            top_master_champ_info = champ_list[top_master_champ_info]

            # API image urls
            img_url = f"http://ddragon.leagueoflegends.com/cdn/{champions_version}/img/champion/{top_master_champ_info['id']}.png"
            thumb_url = f"http://ddragon.leagueoflegends.com/cdn/{champions_version}/img/profileicon/{summoner['profileIconId']}.png"

            # set initals to embed
            embed = Embed(title=f"{summoner['name']}'s LOL Mastery!",
                        description=f"Summoner Level: {summoner['summonerLevel']}",
                        colour=ctx.author.colour)
            # set image to embed
            embed.set_image(url=img_url)
            embed.set_thumbnail(url=thumb_url)
            # add a new field to the embed
            # set variables for fields to embed
            fields = [("Total Champion Mastery Score:", f"*{total_mastery}*", False),
                    ("Highest Mastery Champion:", f"*{top_master_champ_info['name']}*", False),
                    ("Mastery Level:", f"*{top_mastery['championLevel']}*", True),
                    ("Mastery Points:", f"*{top_mastery['championPoints']}*", True)]
            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(lolprofile(bot))