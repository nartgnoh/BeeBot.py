# *********************************************************************************************************************
# gamesmodule.py
# - blackjack command
# *********************************************************************************************************************

import os
import discord
import random
import numpy as np
import json
import cogs.helper.helper_functions.games as games

from discord.ext import commands
from discord.ext.commands import Cog
from discord.utils import get
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
    @commands.command(name='blackjack', aliases=['playblackjack', '♠️'],
                      help='♠️ Play a game of blackjack with BeeBot!'
                      '[React 🇭 to Hit or 🇸 to Stand]')
    async def blackjack(self, ctx):
        games_data = games.get_games_json()
        beebot_profiles_data.setdefault('games', [])
        # user_champ_pool = user_profile.setdefault(CHAMP_POOL_KEY, {})
        # role_champ_pool = user_champ_pool.setdefault(role, [])

        # *********
        # | embed |
        # *********
        embed = Embed(title="♠️ ♥️ Blackjack ♦️ ♣️",
                      description="React 🇭 to Hit or 🇸 to Stand",
                      colour=ctx.author.colour)
        msg = await ctx.send(embed=embed)
        await msg.add_reaction('🇭')
        await msg.add_reaction('🇸')

    # **********************************************
    # | listener on_raw_reaction_add for Blackjack |
    # **********************************************
    @Cog.listener()
    async def on_raw_reaction_add(self, payload):
        message = await self.bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
        reaction = get(message.reactions, emoji=payload.emoji.name)

        if payload.emoji.name == '🇭' and payload.member != self.bot.user:
            embed = Embed(title="♠️ ♥️ Blackjack ♦️ ♣️",
                          description="React 🇭 to Hit or 🇸 to Stand",
                          colour=payload.member.colour)
            embed.add_field(name="THIS IS AN EDIT", value='hello')
            await reaction.remove(payload.member)
            await message.edit(embed=embed)

        # if payload.emoji.name == '🇸' and payload.member != self.bot.user:
        #     if 

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
