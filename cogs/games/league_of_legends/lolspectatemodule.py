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
                            region, summoner['id'])
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
                    new_participants_list = []
                    for participant in spectator['participants']:
                        participant_summoner_id = participant['summonerId']
                        # get ranks
                        ranks = lol_watcher.league.by_summoner(
                            region, participant_summoner_id)
                        for rank in ranks:
                            if 'RANKED_SOLO_5x5' in rank.values():
                                participant['rank'] = rank
                                break
                        # get masteries
                        masteries = lol_watcher.champion_mastery.by_summoner(
                            region, participant_summoner_id)
                        participant['masteries'] = masteries
                        # get current champion
                        for champion in champ_list:
                            if participant['championId'] == int(champ_list[champion]['key']):
                                participant['currentChampion'] = champ_list[champion]
                            if 'top_mastery' in participant and 'currentChampion' in participant:
                                break
                        # add to new_participants_list
                        new_participants_list.append(participant)
                    if spectator['gameMode'] == 'CLASSIC':
                        spectator['gameMode'] = 'Summoner\'s Rift'
                    else:
                        spectator['gameMode'] = spectator['gameMode'].replace(
                            '_', ' ').title()
                    # find your teamid
                    summoner_team_id = 0
                    for participant in new_participants_list:
                        if participant['summonerId'] == summoner['id']:
                            summoner_team_id = participant['teamId']
                            break
                    # # API full rune info
                    # response = requests.get(
                    #     f'http://ddragon.leagueoflegends.com/cdn/{champions_version}/data/en_US/runesReforged.json')
                    # rune_info = response.json()
                    # *********
                    # | embed |
                    # *********
                    embed = Embed(title=f"{summoner['name']}'s Live Game Info",
                                  description=f"Game Mode: {spectator['gameMode']}\n(⭐ Enemies with high mastery on their champion >200k)",
                                  colour=ctx.author.colour)
                    # embed thumbnail
                    thumb_url = f"http://ddragon.leagueoflegends.com/cdn/{champions_version}/img/profileicon/{summoner['profileIconId']}.png"
                    thumb_image = images.get_image_by_url(thumb_url)
                    thumb_image = images.resize_image(thumb_image, 50, 50)
                    images.save_image(thumb_image, images.get_image_path(
                        'riot_images/spectator/thumbnail.png'))
                    file = discord.File(
                        f"resource_files/image_files/riot_images/spectator/thumbnail.png", filename="image.png")
                    embed.set_thumbnail(url='attachment://image.png')
                    # embed fields
                    enemy_team = []
                    enemy_team_rank_wr = []
                    summoner_team = []
                    summoner_team_rank_wr = []
                    enemy_team_high_mastery = []
                    # summoner_runes_image_path = images.get_image_path(
                    #     'riot_images/spectator/runes.png')
                    for participant in new_participants_list:
                        # # summoner runes
                        # if participant['summonerId'] == summoner['id']:
                        #     ddragon_images_url = 'https://ddragon.canisback.com/img/'
                        #     rune_style_id = participant['perks']['perkStyle']
                        #     rune_substyle_id = participant['perks']['perkSubStyle']
                        #     for rune in rune_info:
                        #         if rune['id'] == rune_style_id:
                        #             rune_style_image_url = rune['icon']
                        #         if rune['id'] == rune_substyle_id:
                        #             rune_substyle_image_url = rune['icon']
                        #     rune_style_image = images.get_image_by_url(
                        #         ddragon_images_url + rune_style_image_url)
                        #     rune_substyle_image = images.get_image_by_url(
                        #         ddragon_images_url + rune_substyle_image_url)
                        #     images.merge_images_width_wise(
                        #         rune_style_image, rune_substyle_image, summoner_runes_image_path)
                        # summoner's team
                        if participant['teamId'] == summoner_team_id:
                            # Your Team section
                            summoner_team = summoner_team + \
                                [f"**{participant['summonerName']} - {participant['currentChampion']['name']}**"]
                            if 'rank' in participant:
                                participant_rank = participant['rank']
                                if participant_rank['tier'] == "PLATINUM":
                                    participant_rank['tier'] = "PLAT"
                                elif participant_rank['tier'] == "DIAMOND":
                                    participant_rank['tier'] = "DIA"
                                elif participant_rank['tier'] == "GRANDMASTER":
                                    participant_rank['tier'] = "G M"
                                rank_string = f"Rank: **{participant_rank['tier'].title()} {participant_rank['rank']}** - WR: **{round(participant_rank['wins']/(participant_rank['wins']+participant_rank['losses'])*100, 2)}%** ({participant_rank['wins']}W:{participant_rank['losses']}L)"
                            else:
                                rank_string = "Rank: Unranked"
                            summoner_team_rank_wr = summoner_team_rank_wr + \
                                [rank_string]
                        # enemy team
                        else:
                            # Enemy Team section
                            if 'rank' in participant:
                                participant_rank = participant['rank']
                                if participant_rank['tier'] == "PLATINUM":
                                    participant_rank['tier'] = "PLAT"
                                elif participant_rank['tier'] == "DIAMOND":
                                    participant_rank['tier'] = "DIA"
                                elif participant_rank['tier'] == "GRANDMASTER":
                                    participant_rank['tier'] = "G M"
                                rank_string = f"Rank: **{participant_rank['tier'].title().replace(' ', '')} {participant_rank['rank']}** - WR: **{round(participant_rank['wins']/(participant_rank['wins']+participant_rank['losses'])*100, 2)}%** ({participant_rank['wins']}W:{participant_rank['losses']}L)"
                            else:
                                rank_string = "Rank: Unranked"
                            enemy_team_rank_wr = enemy_team_rank_wr + \
                                [rank_string]
                            # Enemy Team High Mastery section
                            high_mastery = False
                            for mastery in participant['masteries']:
                                if participant['championId'] == mastery['championId']:
                                    if mastery['championPoints'] > 200000:
                                        high_mastery = True
                                        enemy_team = enemy_team + \
                                            [f"⭐ **{participant['summonerName']} - {participant['currentChampion']['name']}**"]
                                    break
                            if not high_mastery:
                                enemy_team = enemy_team + \
                                    [f"**{participant['summonerName']} - {participant['currentChampion']['name']}**"]
                    enemy_team_high_mastery = [
                        i for i in enemy_team_high_mastery if i]
                    embed.add_field(name='Enemy Team:',
                                    value='\n'.join(enemy_team)+'\n\n**Your Team:**\n'+'\n'.join(summoner_team), inline=True)
                    embed.add_field(name='\u200b',
                                    value='\n'.join(enemy_team_rank_wr)+'\n\n\u200b\n'+'\n'.join(summoner_team_rank_wr), inline=True)
                    # embed.add_field(name="Your Runes:",
                    #                 value='\u200b', inline=False)
                    # # embed image
                    # file = discord.File(
                    #     f'resource_files/image_files/riot_images/spectator/runes.png', filename="image.png")
                    # embed.set_image(url='attachment://image.png')
                    msg = await ctx.send(file=file, embed=embed)
                    images.delete_image(images.get_image_path(
                        'riot_images/spectator/thumbnail.png'))
                    await msg.add_reaction("❌")

    # *********************************************************************************************************************
    # bot command test
    # *********************************************************************************************************************

    @commands.command(name='imagetest')
    # only specific roles can use this command
    @commands.has_role(admin_specific_command_name)
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

        images.merge_images_width_wise(image1, image2, images.get_image_path(
            'riot_images/spectator/new_image.png'))

        image1 = images.new_blank_image()
        image2 = images.get_image_by_url(image2_url)

        images.merge_images_width_wise(image1, image2, images.get_image_path(
            'riot_images/spectator/new_image2.png'))

        await ctx.send("images")


def setup(bot):
    bot.add_cog(lolspectatemodule(bot))
