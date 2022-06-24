# *********************************************************************************************************************
# lolprofilemodule.py
# - lol_profile command
# - lol_mastery command
# - lol_rank command
# *********************************************************************************************************************

import os
import discord
import cogs.helper.constants.lol_constants as lol_constants
import cogs.helper.api.league_of_legends_api as lol_api

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

# role specific names
role_specific_command_name = 'Bot Commander'
admin_specific_command_name = 'Bot Admin'

# lolprofilemodule class


class lolprofilemodule(commands.Cog, name="LoLProfileModule", description="lolprofile, lolmastery, lolrank"):
    def __init__(self, bot):
        self.bot = bot

    # *********************************************************************************************************************
    # bot command to show the full profile of a given summoner name (shows rank and mastery)
    # *********************************************************************************************************************
    @commands.command(name='lolprofile', aliases=['profilelol', 'lolp', 'plol', '👤'],
                      help=f"👤 Showcase a summoner\'s league of legends profile.\n\n"
                      f"[Input Region: type \"region:<region>\" (ex: region:kr)]\n"
                      f"[Valid Regions: {', '.join(lol_constants.riot_regions())}]")
    # only specific roles can use this command
    @commands.has_role(role_specific_command_name)
    async def lol_profile(self, ctx, region: Optional[str], *summoner_name):
        summoner_name = list(summoner_name)
        # check region
        region_check = True
        if region == None:
            return await ctx.send("Sorry! You forgot to add any input! :cry: Please try again! :slight_smile:\n")
        if ":" in region:
            region = region[7:]
            if region not in lol_constants.riot_regions():
                region_check = False
                return await ctx.send(f"Sorry! An error has occurred! :cry: Check that you have a valid region! :slight_smile:\n"
                                      f"[Valid Regions: {', '.join(lol_constants.riot_regions())}]")
        else:
            if summoner_name == None:
                summoner_name = region
            else:
                summoner_name = [region] + summoner_name
            region = default_region
        if region_check:
            if not summoner_name:
                return await ctx.send("Sorry! You forgot to add a summoner name! :cry: Please try again! :slight_smile:")
            # check that summoner_name exists
            summoner_check = True
            try:
                # get summoner info
                summoner = lol_watcher.summoner.by_name(
                    region, f"{''.join(summoner_name)}")
            except:
                summoner_check = False
                return await ctx.send("Sorry! The summoner name you inputed doesn't exist! :cry:\n"
                                      "Please try again with a real lol summoner! :slight_smile:")
        if summoner_check:
            # get current lol version for region
            champions_version = lol_api.get_version(region)[
                'n']['champion']
            # get summoner ranks
            ranks = lol_watcher.league.by_summoner(
                region, summoner['id'])
            # get total mastery
            total_mastery = lol_watcher.champion_mastery.scores_by_summoner(
                region, summoner['id'])
            # get top mastery
            top_mastery = lol_watcher.champion_mastery.by_summoner(region, summoner['id'])[
                0]
            # get top mastery champ
            champ_list = lol_api.get_champion_list(
                champions_version)['data']
            top_master_champ_info = ''
            for champion in champ_list:
                if top_mastery['championId'] == int(champ_list[champion]['key']):
                    top_master_champ_info = champion
                    break
            top_master_champ_info = champ_list[top_master_champ_info]
            # *********
            # | embed |
            # *********
            embed = Embed(title=f"{summoner['name']}'s LoL Profile",
                          description=f"Summoner Level: {summoner['summonerLevel']}",
                          colour=ctx.author.colour)
            # embed thumbnail
            thumb_url = f"http://ddragon.leagueoflegends.com/cdn/{champions_version}/img/profileicon/{summoner['profileIconId']}.png"
            embed.set_thumbnail(url=thumb_url)
            # embed fields
            if ranks:
                for rank in ranks:
                    embed.add_field(name=f"{rank['queueType']} Rank:".replace("_", " ").title(),
                                    value=f"{rank['tier'].title()} {rank['rank']} {rank['leaguePoints']}LP\n" +
                                    f"WR: {round((rank['wins']/(rank['wins']+rank['losses']))*100, 2)}% (W{rank['wins']}:L{rank['losses']})", inline=False)
                embed.add_field(
                    name='\u200b', value='\u200b', inline=False)
            fields = [("Total Champion Mastery Score:", f"*{total_mastery}*", False),
                      ("Highest Mastery Champion:",
                       f"*{top_master_champ_info['name']}*", False),
                      ("Mastery Level:",
                       f"*{top_mastery['championLevel']}*", True),
                      ("Mastery Points:", f"*{top_mastery['championPoints']}*", True)]
            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)
            await ctx.send(embed=embed)

    # *********************************************************************************************************************
    # bot command to show the mastery of a given summoner name
    # *********************************************************************************************************************
    @commands.command(name='lolmastery', aliases=['masterylol', 'lolm', 'mlol', '🎓'],
                      help=f"🎓 Showcase a summoner\'s league of legends mastery.\n\n"
                      f"[Input Region: type \"region:<region>\" (ex: region:kr)]\n"
                      f"[Valid Regions: {', '.join(lol_constants.riot_regions())}]")
    # only specific roles can use this command
    @commands.has_role(role_specific_command_name)
    async def lol_mastery(self, ctx, region: Optional[str], *summoner_name):
        summoner_name = list(summoner_name)
        # check region
        region_check = True
        if region == None:
            return await ctx.send("Sorry! You forgot to add any input! :cry: Please try again! :slight_smile:\n")
        if ":" in region:
            region = region[7:]
            if region not in lol_constants.riot_regions():
                region_check = False
                return await ctx.send(f"Sorry! An error has occurred! :cry: Check that you have a valid region! :slight_smile:\n"
                                      f"[Valid Regions: {', '.join(lol_constants.riot_regions())}]")
        else:
            if summoner_name == None:
                summoner_name = region
            else:
                summoner_name = [region] + summoner_name
            region = default_region
        if region_check:
            if not summoner_name:
                return await ctx.send("Sorry! You forgot to add a summoner name! :cry: Please try again! :slight_smile:")
            # check that summoner_name exists
            summoner_check = True
            try:
                # get summoner info
                summoner = lol_watcher.summoner.by_name(
                    region, f"{''.join(summoner_name)}")
            except:
                summoner_check = False
                return await ctx.send("Sorry! The summoner name you inputed doesn't exist! :cry:\n"
                                      "Please try again with a real lol summoner! :slight_smile:")
        if summoner_check:
            # get current lol version for region
            champions_version = lol_api.get_version()['n']['champion']
            # get total mastery
            total_mastery = lol_watcher.champion_mastery.scores_by_summoner(
                region, summoner['id'])
            # get top mastery
            top_mastery = lol_watcher.champion_mastery.by_summoner(region, summoner['id'])[
                0]
            # get top mastery champ
            champ_list = lol_api.get_champion_list(
                champions_version)['data']
            top_master_champ_info = ''
            for champion in champ_list:
                if top_mastery['championId'] == int(champ_list[champion]['key']):
                    top_master_champ_info = champion
                    break
            top_master_champ_info = champ_list[top_master_champ_info]
            # *********
            # | embed |
            # *********
            embed = Embed(title=f"{summoner['name']}'s LoL Mastery",
                          description=f"Summoner Level: {summoner['summonerLevel']}",
                          colour=ctx.author.colour)
            # embed thumbnail
            thumb_url = f"http://ddragon.leagueoflegends.com/cdn/{champions_version}/img/champion/{top_master_champ_info['id']}.png"
            embed.set_thumbnail(url=thumb_url)
            # embed fields
            fields = [("Total Champion Mastery Score:", f"*{total_mastery}*", False),
                      ("Highest Mastery Champion:",
                       f"*{top_master_champ_info['name']}*", False),
                      ("Mastery Level:",
                       f"*{top_mastery['championLevel']}*", True),
                      ("Mastery Points:", f"*{top_mastery['championPoints']}*", True)]
            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)
            await ctx.send(embed=embed)

    # *********************************************************************************************************************
    # bot command to show the rank of a given summoner name
    # *********************************************************************************************************************
    @commands.command(name='lolrank', aliases=['ranklol', 'lolr', 'rlol', '🏆'],
                      help=f"🏆 Showcase a summoner\'s league of legends rank.\n\n"
                      f"[Input Region: type \"region:<region>\" (ex: region:kr)]\n"
                      f"[Valid Regions: {', '.join(lol_constants.riot_regions())}]")
    # only specific roles can use this command
    @commands.has_role(role_specific_command_name)
    async def lol_rank(self, ctx, region: Optional[str], *summoner_name):
        summoner_name = list(summoner_name)
        # check region
        region_check = True
        if region == None:
            return await ctx.send("Sorry! You forgot to add any input! :cry: Please try again! :slight_smile:\n")
        if ":" in region:
            region = region[7:]
            if region not in lol_constants.riot_regions():
                region_check = False
                return await ctx.send(f"Sorry! An error has occurred! :cry: Check that you have a valid region! :slight_smile:\n"
                                      f"[Valid Regions: {', '.join(lol_constants.riot_regions())}]")
        else:
            if summoner_name == None:
                summoner_name = region
            else:
                summoner_name = [region] + summoner_name
            region = default_region
        if region_check:
            if not summoner_name:
                return await ctx.send("Sorry! You forgot to add a summoner name! :cry: Please try again! :slight_smile:")
            # check that summoner_name exists
            summoner_check = True
            try:
                # get summoner info
                summoner = lol_watcher.summoner.by_name(
                    region, f"{''.join(summoner_name)}")
            except:
                summoner_check = False
                return await ctx.send("Sorry! The summoner name you inputed doesn't exist! :cry:\n"
                                      "Please try again with a real lol summoner! :slight_smile:")
        if summoner_check:
            # get current lol version for region
            champions_version = lol_api.get_version(region)[
                'n']['champion']
            # get summoner ranks
            ranks = lol_watcher.league.by_summoner(
                region, summoner['id'])
            # *********
            # | embed |
            # *********
            embed = Embed(title=f"{summoner['name']}'s LoL Rank",
                          description=f"Summoner Level: {summoner['summonerLevel']}",
                          colour=ctx.author.colour)
            if ranks:
                riot_ranks = lol_constants.riot_ranks()
                total_rank = 0
                for rank in ranks:
                    embed.add_field(name=f"{rank['queueType']} Rank:".replace("_", " ").title(),
                                    value=f"{rank['tier'].title()} {rank['rank']} {rank['leaguePoints']}LP\n" +
                                    f"WR: {round((rank['wins']/(rank['wins']+rank['losses']))*100, 2)}% (W{rank['wins']}:L{rank['losses']})", inline=False)
                    # get average_rank
                    rank_key = [k for k, v in riot_ranks.items(
                    ) if v == {'tier': rank['tier'], 'rank': rank['rank']}]
                    total_rank = total_rank + sum(rank_key)
                average_rank = round(total_rank/len(ranks), 0)
                final_rank = riot_ranks.get(int(average_rank))

                embed.add_field(
                    name=f"Average Rank:", value=f"{final_rank['tier'].title()} {final_rank['rank']}", inline=False)
                # embed thumbnail
                file = discord.File(
                    f"resource_files/image_files/riot_images/ranked_emblems/Emblem_{final_rank['tier'].title()}.png", filename="image.png")
                embed.set_thumbnail(url='attachment://image.png')
                await ctx.send(file=file, embed=embed)
            else:
                embed.add_field(name="This summoner has nothing for ranked this season.",
                                value="Maybe it's time?... 👀", inline=False)
                # embed thumbnail
                thumb_url = f"http://ddragon.leagueoflegends.com/cdn/{champions_version}/img/map/map11.png"
                embed.set_thumbnail(url=thumb_url)
                await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(lolprofilemodule(bot))
