# *********************************************************************************************************************
# gamesmodule.py
# - blackjack command
# *********************************************************************************************************************

import os
import discord
import random
import numpy as np
import json
import cogs.helper.constants.emoji_constants as emoji_constants

from discord.ext import commands
from discord import Embed
from typing import Optional

# get current directory
current_directory = os.path.dirname(os.path.realpath(__file__))
# role specific names
role_specific_command_name = 'Bot Commander'
admin_specific_command_name = 'Bot Admin'

# gamesmodule class


class gamesmodule(commands.Cog, name="GamesModule", description="blackjack, coinflip, diceroll"):
    def __init__(self, bot):
        self.bot = bot

    # *********************************************************************************************************************
    # bot command to pick a game from an excel sheet of games with number of player specification
    # *********************************************************************************************************************
    @commands.command(name='playblackjack', aliases=['blackjack', '♠️'],
                      help='🎮 Picks a game to play. [Auto: Number of people in voice channel]')
    async def blackjack(self, ctx, number_of_players: Optional[int]):
        if number_of_players == None:
            # else number_of_players was 0
            if ctx.message.author.voice is None:
                return await ctx.send('An error occurred! :thinking:\nTry adding a number after "pickgame" '
                                      'or joining a voice channel! :slight_smile:')
            # if "number_of_players" is none, then get the "number_of_players" in the voice channel of the author
            channel = ctx.message.author.voice.channel
            number_of_players = len(channel.members)
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
                          colour=discord.Colour.random())
        # embed without url
        else:
            embed = Embed(title=random_game,
                          description=pg_message,
                          colour=discord.Colour.random())
        await ctx.send(embed=embed)

    # *********************************************************************************************************************
    # bot command to flip coin
    # *********************************************************************************************************************
    @commands.command(name='coinflip', aliases=['coin', 'coins', 'flip', 'flips', '🟡'],
                      help='🟡 Simulates coin flip. [Max coins: 100]')
    async def coin_flip(self, ctx, number_of_coins: Optional[int]):
        cf_results = ''
        # default 1 coin
        if number_of_coins == None:
            number_of_coins = 1
        if number_of_coins > 100 or number_of_coins < 1:
            return await ctx.send('Sorry! Your number is out of bounds! :cry: Try again! [Max coins: 100]')
        coin_flip_ht = [
            'Heads, ',
            'Tails, '
        ]
        cf_quotes = [
            'You coin flip(s) were:',
            'Clink, spin, spin, clink:',
            'Heads or Tails? :open_mouth:',
            'I wish you good RNG :relieved:',
            ':coin:'
        ]
        cf_message = random.choice(cf_quotes)
        # add coin flips to string
        for i in range(number_of_coins):
            cf_results = cf_results + random.choice(coin_flip_ht)
        # *********
        # | embed |
        # *********
        embed = Embed(title=cf_message,
                      colour=discord.Colour.gold(),
                      description=cf_results[:-2])

        await ctx.send(embed=embed)

    # *********************************************************************************************************************
    # bot command to roll dice (no specification is an auto 1D6)
    # *********************************************************************************************************************
    @commands.command(name='diceroll', aliases=['rolldice', 'roll', 'dice', '🎲'],
                      help='🎲 Simulates rolling dice. [Auto: 1D6, Max dice: 100D100]')
    async def dice_roll(self, ctx, number_of_dice: Optional[int], number_of_sides: Optional[int]):
        # default 1D6 dice
        if number_of_dice == None:
            number_of_dice = 1
        if number_of_sides == None:
            number_of_sides = 6
        if number_of_dice > 100 or number_of_dice < 1 or number_of_sides > 100 or number_of_sides < 1:
            return await ctx.send('Sorry! Your number(s) are out of bounds! :cry: Try again! [Max dice: 100D100]')
        dice = [
            str(random.choice(range(1, number_of_sides + 1)))
            for _ in range(number_of_dice)
        ]
        rd_quotes = [
            'Your dice roll(s) were:',
            'Clack, rattle, clatter:',
            'Highroller?!? :open_mouth:',
            'I wish you good RNG :relieved:',
            ':game_die:',
            ':skull: + :ice_cube:'
        ]
        rd_message = random.choice(rd_quotes)
        # *********
        # | embed |
        # *********
        embed = Embed(title=rd_message,
                      colour=discord.Colour.random(),
                      description=', '.join(dice))
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(gamesmodule(bot))
