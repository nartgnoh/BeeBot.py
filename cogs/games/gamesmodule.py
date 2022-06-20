# *********************************************************************************************************************
# gamesmodule.py
# - split_teams command
# - pick_game command
# *********************************************************************************************************************

from ast import alias
import os
import discord
import random
import numpy as np
import json

from discord.ext import commands
from discord import Embed
from typing import Optional

# get current directory
current_directory = os.path.dirname(os.path.realpath(__file__))
# role specific names
role_specific_command_name = 'Bot Commander'
admin_specific_command_name = 'Bot Admin'

# gamesmodule class


class gamesmodule(commands.Cog, name="GamesModule", description="spiltteams, pickgame"):
    def __init__(self, bot):
        self.bot = bot

    # *********************************************************************************************************************
    # bot command to split teams
    # *********************************************************************************************************************
    @commands.command(name='splitteams', aliases=['teamsplit', 'maketeams', 'maketeam', 'pickteams', 'pickteam', 'teams', 'team', 'bbb', '📋'],
                      help='📋 Splits members in voice channel into teams.\n[Auto: 2, Max teams: 101]')
    async def split_teams(self, ctx, number_of_teams: Optional[int]):
        # check for members in voice call
        if ctx.message.author.voice is None:
            await ctx.send('An error has occurred! :confounded: Try joining a voice channel! :slight_smile:')
        else:
            # set "number_of_teams" to 2 if none
            if number_of_teams == None:
                number_of_teams = 2
            # check if in bounds
            if number_of_teams > 101 and number_of_teams < 0:
                await ctx.send('Sorry! Your number is out of bounds! :cry: Try again! [Max teams: 101]')
            else:
                # create a "players_list" for members in the voice channel
                channel = ctx.message.author.voice.channel
                players_list = []
                for member in channel.members:
                    user = member.display_name
                    players_list.append(user)
                # randomize the elements of the list 1 to "len(channel.members)" times
                for i in range(random.randint(1, len(channel.members))):
                    random.shuffle(players_list)
                # split the teams into the number of teams
                team_split = np.array_split(players_list, number_of_teams)
                teams_dict = {}
                team_number = 0
                for team in team_split:
                    team_number += 1
                    teams_dict[team_number] = list(team)
                # *********
                # | embed |
                # *********
                embed = Embed(title="The Teams:",
                              colour=ctx.author.colour)
                for team in teams_dict:
                    # check if list is empty
                    if teams_dict[team]:
                        # embed fields
                        embed.add_field(
                            name=f"Team {team}:", value=f"{', '.join(teams_dict[team])}", inline=False)
                await ctx.send(embed=embed)

    # *********************************************************************************************************************
    # bot command to pick a game from an excel sheet of games with number of player specification
    # *********************************************************************************************************************
    @commands.command(name='pickgame', aliases=['🎮', 'pickgames'], help='🎮 Picks a game to play. [Auto: Number of people in voice channel]')
    async def pick_game(self, ctx, number_of_players: Optional[int]):
        if number_of_players == None:
            if ctx.message.author.voice is not None:
                # if "number_of_players" is none, then get the "number_of_players" in the voice channel of the author
                channel = ctx.message.author.voice.channel
                number_of_players = len(channel.members)
            # else number_of_players was 0
            else:
                await ctx.send('An error occurred! :thinking:\nTry adding a number after "pickgame" '
                               'or joining a voice channel! :slight_smile:')
        # get games.json file
        games_json_path = "/".join(list(current_directory.split('/')
                                   [0:-2])) + '/resource_files/json_files/games.json'
        with open(games_json_path) as games_json:
            games = json.load(games_json)
            final_games_list = []
            # iterate through games dictionary
            for key in games:
                if games[key]['min'] <= number_of_players and games[key]['max'] >= number_of_players:
                    final_games_list.append(key)
            # picking a random game from the final_games_list
            random_game = random.choice(final_games_list)
            url = games[random_game]['url']
        pg_quotes = [f'Have you tried *{random_game}*? :smile:',
                     f'Why not try *{random_game}*? :open_mouth:',
                     f'I recommend *{random_game}*! :liar:',
                     f'I might not have friends, but your friends can play *{random_game}*! :smiling_face_with_tear:']
        pg_message = random.choice(pg_quotes)
        # *********
        # | embed |
        # *********
        # create an embed with game url
        if url is not None:
            embed = Embed(title=random_game,
                          url=url,
                          description=pg_message,
                          colour=ctx.author.colour)
        # embed without url
        else:
            embed = Embed(title=random_game,
                          description=pg_message,
                          colour=ctx.author.colour)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(gamesmodule(bot))
