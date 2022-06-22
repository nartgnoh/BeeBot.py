# *********************************************************************************************************************
# lolspectatemodule.py
# - pick_skin command
# *********************************************************************************************************************

import os
import discord
import random
import requests
import cogs.helper.constants.lol_constants as lol_constants
import cogs.helper.api.league_of_legends_api as lol_api
import cogs.helper.helper_functions.images as images

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

# lolspectatemodule class


class lolspectatemodule(commands.Cog, name="LoLSpectateModule", description="lolspectate"):
    def __init__(self, bot):
        self.bot = bot

    # *********************************************************************************************************************
    # bot command pick a random skin for champion
    # *********************************************************************************************************************
    @commands.command(name='lolspectate', aliases=['spectatelol', 'lolcurrent', 'currentlol', '🕵️'],
                      help="🕵️ Lookup a current game!\n\n"
                      f"[Input Region: type \"region:<region>\" (ex: region:kr)]\n"
                      f"[Valid Regions: {', '.join(lol_constants.riot_regions())}]")
    # only specific roles can use this command
    @commands.has_role(role_specific_command_name)
    async def lol_profile(self, ctx, region: Optional[str], *summoner_name):
        summoner_name = list(summoner_name)
        # check region
        region_check = True
        if region == None:
            await ctx.send("Sorry! You forgot to add any input! :cry: Please try again! :slight_smile:\n")
        else:
            if ":" in region:
                region = region[7:]
                if region not in lol_constants.riot_regions():
                    region_check = False
                    await ctx.send(f"Sorry! An error has occurred! :cry: Check that you have a valid region! :slight_smile:\n"
                                   f"[Valid Regions: {', '.join(lol_constants.riot_regions())}]")
            else:
                if summoner_name == None:
                    summoner_name = region
                else:
                    summoner_name = [region] + summoner_name
                region = default_region
            if region_check:
                if not summoner_name:
                    await ctx.send("Sorry! You forgot to add a summoner name! :cry: Please try again! :slight_smile:")
                else:
                    # check that summoner_name exists
                    summoner_check = True
                    try:
                        # get summoner info
                        summoner = lol_watcher.summoner.by_name(
                            region, f"{''.join(summoner_name)}")
                    except:
                        summoner_check = False
                        await ctx.send("Sorry! The summoner name you inputed doesn't exist! :cry:\n"
                                       "Please try again with a real lol summoner! :slight_smile:")
                    # check that spectator game exists
                    spectator_check = True
                    try:
                        # get spectator info
                        spectator = lol_watcher.spectator.by_summoner(
                            region, f"{''.join(summoner_name)}")
                    except:
                        spectator_check = False
                        await ctx.send("Sorry! The summoner name you inputed isn't currently in a game! :cry:\n"
                                       "Please try again with a current game! :slight_smile:")
                if summoner_check and spectator_check:
                    # get current lol version for region
                    champions_version = lol_api.get_version(region)[
                        'n']['champion']
                    champ_list = lol_api.get_champion_list(
                        champions_version)['data']
                    

                    
                    # image
                    image_path = images.get_image_path('')

                    

                    # # get summoner ranks
                    # ranks = lol_watcher.league.by_summoner(
                    #     region, summoner['id'])
                    # # get total mastery
                    # total_mastery = lol_watcher.champion_mastery.scores_by_summoner(
                    #     region, summoner['id'])
                    # # get top mastery
                    # top_mastery = lol_watcher.champion_mastery.by_summoner(region, summoner['id'])[
                    #     0]
                    # # get top mastery champ
                    # champ_list = lol_api.get_champion_list(
                    #     champions_version)['data']
                    # top_master_champ_info = ''
                    # for champion in champ_list:
                    #     if top_mastery['championId'] == int(champ_list[champion]['key']):
                    #         top_master_champ_info = champion
                    #         break
                    # top_master_champ_info = champ_list[top_master_champ_info]
                    # *********
                    # | embed |
                    # *********
                    # embed = Embed(title=f"{summoner['name']}'s LOL Profile",
                    #               description=f"Summoner Level: {summoner['summonerLevel']}",
                    #               colour=ctx.author.colour)
                    # # embed thumbnail
                    # thumb_url = f"http://ddragon.leagueoflegends.com/cdn/{champions_version}/img/profileicon/{summoner['profileIconId']}.png"
                    # embed.set_thumbnail(url=thumb_url)
                    # # embed fields
                    # if ranks:
                    #     for rank in ranks:
                    #         embed.add_field(name=f"{rank['queueType']} Rank:".replace("_", " ").title(),
                    #                         value=f"{rank['tier'].title()} {rank['rank']} {rank['leaguePoints']}LP\n" +
                    #                         f"Wins: {rank['wins']} Losses: {rank['losses']}", inline=False)
                    #     embed.add_field(
                    #         name='\u200b', value='\u200b', inline=False)
                    # fields = [("Total Champion Mastery Score:", f"*{total_mastery}*", False),
                    #           ("Highest Mastery Champion:",
                    #            f"*{top_master_champ_info['name']}*", False),
                    #           ("Mastery Level:",
                    #            f"*{top_mastery['championLevel']}*", True),
                    #           ("Mastery Points:", f"*{top_mastery['championPoints']}*", True)]
                    # for name, value, inline in fields:
                    #     embed.add_field(name=name, value=value, inline=inline)
                    # await ctx.send(embed=embed)


    
    # *********************************************************************************************************************
    # bot command test
    # *********************************************************************************************************************
    @commands.command(name='imagetest')
    # only specific roles can use this command
    @commands.has_role(role_specific_command_name)
    async def champ_lookup(self, ctx, champ1, champ2):
        # get current lol version for region
        champions_version = lol_api.get_version()['n']['champion']
        champ_list = lol_api.get_champion_list(champions_version)['data']

        lol_champion1 = lol_api.champion_string_formatting(champ1)
        lol_champion2 = lol_api.champion_string_formatting(champ2)

        image1_url = f'http://ddragon.leagueoflegends.com/cdn/{champions_version}/img/champion/{lol_champion1}.png'
        image2_url = f'http://ddragon.leagueoflegends.com/cdn/{champions_version}/img/champion/{lol_champion2}.png'

        image1 = images.get_image_by_url(image1_url)
        image2 = images.get_image_by_url(image2_url)
        
        images.merge_images_width_wise(image1, image2, images.get_image_path('riot_images/spectator/new_image.png'))

        image1 = images.new_blank_image()
        image2 = images.get_image_by_url(image2_url)
        
        images.merge_images_width_wise(image1, image2, images.get_image_path('riot_images/spectator/new_image2.png'))
        
        await ctx.send("images")

def setup(bot):
    bot.add_cog(lolspectatemodule(bot))
