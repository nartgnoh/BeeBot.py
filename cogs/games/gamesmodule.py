# *********************************************************************************************************************
# gamesmodule.py
# - blackjack command
# *********************************************************************************************************************

import os
import discord
import random
import cogs.helper.helper_functions.games as games
import cogs.helper.constants.games_constants as games_constants

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
                      help='♠️ Play a game of blackjack with BeeBot! '
                      '[React 🇭 to Hit or 🇸 to Stand]')
    async def blackjack(self, ctx):
        blackjack_deck = games_constants.blackjack_cards()
        active_cards = random.sample(list(blackjack_deck), 4)
        # dealer
        dealer_cards = {active_cards[0]: blackjack_deck[active_cards[0]],
                        active_cards[2]: blackjack_deck[active_cards[2]]}
        dealer_message = f"1: **{list(dealer_cards)[0]}**\n2: **???**"
        # player
        player_cards = {active_cards[1]: blackjack_deck[active_cards[1]],
                        active_cards[3]: blackjack_deck[active_cards[3]]}
        player_total = sum(player_cards.values())
        player_message = f"1: **{list(player_cards)[0]}**\n2: **{list(player_cards)[1]}**\nPlayer's Total: **{player_total}**"
        # *********
        # | embed |
        # *********
        embed = Embed(title="♠️ ♥️ Blackjack ♦️ ♣️",
                      description="React 🇭 to Hit or 🇸 to Stand",
                      colour=ctx.author.colour)
        # embed fields
        if player_total == 21:
            while sum(dealer_cards.values()) < 17:
                inactive_cards = [e for e in list(
                    blackjack_deck) if e not in active_cards]
                new_card = random.choice(inactive_cards)
                [blackjack_deck][new_card] = blackjack_deck[new_card]
                active_cards = active_cards + [new_card]
                if sum(dealer_cards.values()) > 21:
                    for key in dealer_cards:
                        if dealer_cards[key] == 11:
                            dealer_cards[key] = 1
                        if sum(dealer_cards.values()) <= 21:
                            break
            # dealer message
            dealer_message = ''
            d_count = 0
            for card in dealer_cards:
                d_count += 1
                dealer_message = dealer_message + \
                    f"{d_count}: {card}\n"
            dealer_message = dealer_message + \
                f"BeeBot's Total: **{sum(dealer_cards.values())}**"
            embed.add_field(name="Beebot's Cards:",
                            value=dealer_message, inline=False)
            embed.add_field(name="Player's Cards:",
                            value=f"1: **{list(player_cards)[0]}**\n2: **{list(player_cards)[1]}**\n"
                            f"Player's Total: **{player_total}**", inline=False)
            if sum(dealer_cards.values()) == 21:
                embed.add_field(name="Winners:",
                                value=f"**Draw!** 😇", inline=False)
            else:
                embed.add_field(name="Winner:",
                                value=f"**{ctx.message.author.display_name} Wins!!** 🥳", inline=False)
            await ctx.send(embed=embed)
        else:
            if player_total == 22:
                player_total = player_total - 10
                player_cards[list(player_cards)[0]] = 1
                player_message = f"1: **{list(player_cards)[0]}**\n2: **{list(player_cards)[1]}**\nPlayer's Total: **{player_total}**"
            embed.add_field(name="BeeBot's Cards:",
                            value=dealer_message, inline=False)
            embed.add_field(name="Player's Cards:",
                            value=player_message, inline=False)
            msg = await ctx.send(embed=embed)
            await msg.add_reaction('🇭')
            await msg.add_reaction('🇸')
            # save blackjack game in games.json
            games_data = games.get_games_json()
            games_data.setdefault('blackjack', {})
            games_data['blackjack'][int(msg.id)] = {'author_name': str(ctx.message.author),
                                                    'dealer_cards': dealer_cards,
                                                    'dealer_message': dealer_message,
                                                    'player_cards': player_cards,
                                                    'player_message': player_message,
                                                    'all_active_cards_list': active_cards}
            games.set_games_json(games_data)

    # **********************************************
    # | listener on_raw_reaction_add for Blackjack |
    # **********************************************
    @Cog.listener()
    async def on_raw_reaction_add(self, payload):
        message = await self.bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
        reaction = get(message.reactions, emoji=payload.emoji.name)
        if (payload.emoji.name == '🇭' or payload.emoji.name == '🇸') and payload.member != self.bot.user:
            games_data = games.get_games_json()
            games_data.setdefault('blackjack', {})
            if str(payload.message_id) in games_data['blackjack']:
                blackjack_game = games_data['blackjack'][str(
                        payload.message_id)]
                if str(payload.member) == blackjack_game['author_name']:
                    # get info
                    blackjack_deck = games_constants.blackjack_cards()
                    bust_check = False
                    blackjack_check = False
                    # *******
                    # | Hit |
                    # *******
                    if payload.emoji.name == '🇭':
                        inactive_cards = [e for e in list(
                            blackjack_deck) if e not in blackjack_game['all_active_cards_list']]
                        new_card = random.choice(inactive_cards)
                        blackjack_game['player_cards'][new_card] = blackjack_deck[new_card]
                        blackjack_game['all_active_cards_list'] = blackjack_game['all_active_cards_list'] + [
                            new_card]
                        # player message
                        player_message = ''
                        p_count = 0
                        for card in list(blackjack_game['player_cards']):
                            p_count += 1
                            player_message = player_message + \
                                f"{p_count}: **{card}**\n"
                        # checks
                        if sum(blackjack_game['player_cards'].values()) == 21:
                            blackjack_check = True
                        elif sum(blackjack_game['player_cards'].values()) > 21:
                            bust_check = True
                            for key in blackjack_game['player_cards']:
                                if blackjack_game['player_cards'][key] == 11:
                                    blackjack_game['player_cards'][key] = 1
                                if sum(blackjack_game['player_cards'].values()) <= 21:
                                    bust_check = False
                                    break
                        player_message = player_message + \
                            f"Player's Total: **{sum(blackjack_game['player_cards'].values())}**"
                        blackjack_game['player_message'] = player_message
                        # player hit
                        if not bust_check and not blackjack_check:
                            # *********
                            # | embed |
                            # *********
                            embed = Embed(title="♠️ ♥️ Blackjack ♦️ ♣️",
                                        description="React 🇭 to Hit or 🇸 to Stand",
                                        colour=payload.member.colour)
                            # embed fields
                            embed.add_field(name="BeeBot's Cards:",
                                            value=blackjack_game['dealer_message'], inline=False)
                            embed.add_field(name="Player's Cards:",
                                            value=player_message, inline=False)
                            await message.edit(embed=embed)
                            await reaction.remove(payload.member)
                            games.set_games_json(games_data)
                    # *********
                    # | Stand |
                    # *********
                    if payload.emoji.name == '🇸' or bust_check or blackjack_check:
                        while sum(blackjack_game['dealer_cards'].values()) < 17:
                            inactive_cards = [e for e in list(
                                blackjack_deck) if e not in blackjack_game['all_active_cards_list']]
                            new_card = random.choice(inactive_cards)
                            blackjack_game['dealer_cards'][new_card] = blackjack_deck[new_card]
                            blackjack_game['all_active_cards_list'] = blackjack_game['all_active_cards_list'] + [
                                new_card]
                            if sum(blackjack_game['dealer_cards'].values()) > 21:
                                for key in blackjack_game['dealer_cards']:
                                    if blackjack_game['dealer_cards'][key] == 11:
                                        blackjack_game['dealer_cards'][key] = 1
                                    if sum(blackjack_game['dealer_cards'].values()) <= 21:
                                        break
                        # dealer message
                        dealer_message = ''
                        d_count = 0
                        for card in blackjack_game['dealer_cards']:
                            d_count += 1
                            dealer_message = dealer_message + \
                                f"{d_count}: {card}\n"
                        dealer_message = dealer_message + \
                            f"BeeBot's Total: **{sum(blackjack_game['dealer_cards'].values())}**"
                        # *********
                        # | embed |
                        # *********
                        embed = Embed(title="♠️ ♥️ Blackjack ♦️ ♣️",
                                    colour=payload.member.colour)
                        # embed fields
                        embed.add_field(name="BeeBot's Cards:",
                                        value=dealer_message, inline=False)
                        embed.add_field(name="Player's Cards:",
                                        value=blackjack_game['player_message'], inline=False)
                        dealer_total = sum(blackjack_game['dealer_cards'].values())
                        player_total = sum(blackjack_game['player_cards'].values())
                        if dealer_total > 21 and player_total > 21:
                            embed.add_field(name="Winner:",
                                            value=f"**Everyone Loses. ☹️**", inline=False)
                        elif dealer_total == player_total:
                            embed.add_field(name="Winner:",
                                            value=f"**Draw!** 😇", inline=False)
                        elif (dealer_total > player_total or bust_check) and dealer_total <= 21:
                            embed.add_field(name="Winner:",
                                            value=f"**BeeBot Wins!! 😄**", inline=False)
                        elif dealer_total < player_total or dealer_total > 21:
                            embed.add_field(name="Winner:",
                                            value=f"**{payload.member.display_name} Wins!! 🥳**", inline=False)
                        await message.edit(embed=embed)
                        # remove blackjack game
                        games_data['blackjack'].pop(str(payload.message_id))
                        games.set_games_json(games_data)
                        await message.clear_reactions()

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
