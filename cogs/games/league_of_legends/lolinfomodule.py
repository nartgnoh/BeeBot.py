# *********************************************************************************************************************
# lolinfomodule.py
# - champ_lookup command
# - champ_skills command
# - pick_skin command
# - lol_balance command
# - lol_live_game command
# *********************************************************************************************************************

import os
import discord
import random
import requests
import cogs.helper.helper_functions.images as images
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

# lolinfomodule class


class lolinfomodule(commands.Cog, name="LoLInfoModule",
                    description="champlookup, champskills, lollivegame, lolbalance, pickskin"):
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
            return await ctx.send("Sorry! An error has occurred! :cry: Check your spelling and try again! :slight_smile:")
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
                                                   'schamp', 'champskill', 'skillschamp', 'skillchamp', '💥'],
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
            return await ctx.send("Sorry! An error has occurred! :cry: Check your spelling and try again! :slight_smile:")
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

    # *********************************************************************************************************************
    # bot command pick a random skin for champion
    # *********************************************************************************************************************
    @commands.command(name='pickskin', aliases=['skinlol', 'lolskin', 'skinpick', 'champskin', 'skinchamp',
                                                'skinschamp', 'champskins' '👗'],
                      help='👗 Pick a random skin for a champion! [Auto: random champ]')
    # only specific roles can use this command
    @commands.has_role(role_specific_command_name)
    async def pick_skin(self, ctx, *, lol_champion: Optional[str]):
        # get current lol version for region
        champions_version = lol_api.get_version()['n']['champion']
        champ_list = lol_api.get_champion_list(champions_version)['data']
        if lol_champion == None:
            lol_champion = random.choice(list(champ_list))
        else:
            lol_champion = lol_api.champion_string_formatting(lol_champion)
        if lol_champion not in champ_list:
            return await ctx.send("Sorry! An error has occurred! :cry: Check your spelling and try again! :slight_smile:")
        # API champion info
        response = requests.get(
            f'http://ddragon.leagueoflegends.com/cdn/{champions_version}/data/en_US/champion/{lol_champion}.json')
        champion_info = response.json()['data'][lol_champion]
        # get skin number dict
        num_dict = {}
        for skin in champion_info['skins']:
            num_dict[skin['num']] = skin['name']
        skin_key = random.choice(list(num_dict))
        # *********
        # | embed |
        # *********
        embed = Embed(title=num_dict.get(skin_key),
                      description=champion_info['title'],
                      colour=discord.Colour.random())
        # embed thumbnail
        img_url = f'http://ddragon.leagueoflegends.com/cdn/img/champion/splash/{lol_champion}_{skin_key}.jpg'
        embed.set_thumbnail(url=img_url)
        await ctx.send(embed=embed)

    # *********************************************************************************************************************
    # bot command to balance a league of legends team comp
    # *********************************************************************************************************************
    @commands.command(name='lolbalance', aliases=['balancelol', 'lolteamcomp', 'teamcomplol', 'lolteam',
                                                  'teamlol', 'lolteams', 'teamslol', '⚖️'],
                      help='⚖️ Help balance a lol teamcomp! [Champions with spaces need quotes ""]\n\n'
                      '[Add an "❌" reaction to delete]')
    # only specific roles can use this command
    @commands.has_role(role_specific_command_name)
    async def lol_balance(self, ctx, *lol_champions):
        if not lol_champions:
            return await ctx.send("Sorry! You forgot to add champions! :slight_smile:")
        # get current lol version for region
        champions_version = lol_api.get_version()['n']['champion']
        champ_list = lol_api.get_champion_list(champions_version)['data']
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
            return await ctx.send("Sorry! An error has occurred! :cry: "
                                  "Check your spelling and try again!\n"
                                  "Don't forget to put champions with spaces in quotes \"\"! "
                                  "(ex; \"Miss Fortune\") :slight_smile:")
        all_tags = lol_constants.lol_tags()
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
        embed = Embed(title="Teamcomp Balance",
                      description="Check if your team is well balanced! :D",
                      colour=discord.Colour.random())
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
        msg = await ctx.send(file=file, embed=embed)
        await msg.add_reaction("❌")

    # *********************************************************************************************************************
    # bot command look up stats for a live League of Legends game
    # *********************************************************************************************************************
    @commands.command(name='lollivegame', aliases=['livegamelol', 'lolspectate', 'spectatelol', 'lolcurrent',
                                                   'currentlol', 'lolspec', 'speclol', '🕵️'],
                      help="🕵️ Lookup stats for a live LoL game!\n\n"
                      f"[Input Region: type \"region:<region>\" (ex: region:kr)]\n"
                      f"[Valid Regions: {', '.join(lol_constants.riot_regions())}]")
    # only specific roles can use this command
    @commands.has_role(role_specific_command_name)
    async def lol_live_game(self, ctx, region: Optional[str], *summoner_name):
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
            # check that spectator game exists
            spectator_check = True
            try:
                # get spectator info
                spectator = lol_watcher.spectator.by_summoner(
                    region, summoner['id'])
            except:
                spectator_check = False
                return await ctx.send("Sorry! The summoner name you inputed isn't currently in a League of Legends game! :cry:\n"
                                      "Please try again with a current LoL game! :slight_smile:")
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
                          description=f"Game Mode: {spectator['gameMode']}",
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
                    enemy_team = enemy_team + \
                        [f"**{participant['summonerName']} - {participant['currentChampion']['name']}**"]
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
                    for mastery in participant['masteries']:
                        if participant['championId'] == mastery['championId']:
                            if mastery['championPoints'] > 200000:
                                enemy_team_high_mastery = enemy_team_high_mastery + \
                                    [f"{participant['summonerName']} ({participant['currentChampion']['name']})"]
                            break
            if not enemy_team_high_mastery:
                enemy_team_high_mastery = ['None']
            embed.add_field(name='Enemy Team:',
                            value='\n'.join(enemy_team), inline=True)
            embed.add_field(name='\u200b',
                            value='\n'.join(enemy_team_rank_wr), inline=True)
            embed.add_field(name='Enemies with high mastery on their champion (>200k):',
                            value=', '.join(enemy_team_high_mastery), inline=False)
            embed.add_field(name='Your Team',
                            value='\n'.join(summoner_team), inline=True)
            embed.add_field(name='\u200b',
                            value='\n'.join(summoner_team_rank_wr), inline=True)
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


def setup(bot):
    bot.add_cog(lolinfomodule(bot))
