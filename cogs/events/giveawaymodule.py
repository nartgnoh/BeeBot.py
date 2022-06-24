# *********************************************************************************************************************
# giveawaymodule.py
# - giveaway command
# *********************************************************************************************************************

import os
import discord
import random
import cogs.helper.constants.emoji_constants as emoji_constants
import cogs.helper.helper_functions.emojis as emojis
import cogs.helper.helper_functions.events as events
import cogs.helper.helper_functions.string_formatter as string_formatter

from discord.ext import commands
from discord.ext.commands import Cog
from discord import Embed
from typing import Optional
from datetime import datetime

# role specific names
role_specific_command_name = 'Bot Commander'
admin_specific_command_name = 'Bot Admin'

# giveawaymodule class


class giveawaymodule(commands.Cog, name="GiveawayModule", description="giveaway"):
    def __init__(self, bot):
        self.bot = bot

    # *********************************************************************************************************************
    # bot command to end a giveaway in chat
    # *********************************************************************************************************************
    @commands.command(name='endgiveaway', aliases=['finishgiveaway', '🎉'],
                      help='🎉 End a giveaway you made!')
    # only specific roles can use this command
    @commands.has_role(role_specific_command_name)
    async def create_giveaway(self, ctx, *, title: Optional[str]):
        if title == None:
            return await ctx.send("Sorry! You forgot to add your title! :open_mouth: Please try again! :slight_smile:")
        giveaway_author = str(ctx.message.author)
        events_data = events.get_events_json()
        if not events.check_event(events_data, 'giveaways') or not giveaway_author in events_data['giveaways']:
            return await ctx.send("Sorry! You don't have a giveaway active! :cry:")
        giveaway_check = False
        for giveaway in events_data['giveaways'][giveaway_author]:
            if giveaway['title'] == title:
                giveaway_check = True
                giveaway = giveaway
                break
        if not giveaway_check:
            return await ctx.send("Sorry! You don't have a giveaway active! :cry:")
        print(giveaway)
        reaction = giveaway['reaction']
        days = datetime.now() - giveaway['start_time']
        participants = giveaway['participants']
        rewards = giveaway['rewards']
        events_data['giveaways'][giveaway_author].remove(giveaway)

        # events.set_events_json(events_data)

        # get winners
        party_keys = participants.keys()
        random.shuffle(party_keys)
        winners_list = random.sample(party_keys, len(rewards))
        rewards_list = []
        count = 0
        final_message = ''
        for reward in rewards:
            count += 1
            rewards_list = rewards_list + \
                [f"{string_formatter.make_ordinal(count)} Place: {winners_list(count-1)} ({reward})"]
            final_message = final_message + \
                f"{string_formatter.make_ordinal(count)} Place: <@{participants[winners_list(count-1)]}>"
        # *********
        # | embed |
        # *********
        embed = Embed(title=f"{ctx.author.display_name}'s __{title}__ Giveaway Winners!",
                      colour=ctx.author.colour)
        # embed fields
        embed.add_field(name="Winners:",
                        value='\n'.join(rewards_list), inline=False)
        # embed footer
        embed.set_footer(
            text=f"Giveaway By: {giveaway_author}\n{reaction} This giveaway lasted {days} day(s)!")
        await ctx.send(embed=embed)
        await ctx.send()

    # *********************************************************************************************************************
    # bot command to make a giveaway in chat
    # *********************************************************************************************************************
    @commands.command(name='giveaway', aliases=['creategiveaway', 'makegiveaway', '🎁'],
                      help='🎁 Make a giveaway! [Type "BB help giveaway" for more info, Role specific]\n\n'
                      'Titles with spaces need quotes "".\n'
                      'Prizes must be in a list format in apostrophes \'\' in descending order inside quotes "".\n'
                      'Example:\nBB giveaway "BB Bucks" 💵 "[\'500 BB Bucks\', \'200 BB Bucks\', \'100 BB Bucks\']"\nRules: Be good c:')
    # only specific roles can use this command
    @commands.has_role(role_specific_command_name)
    async def create_giveaway(self, ctx, title: Optional[str], reaction: Optional[str],
                              rewards: Optional[str], *, description: Optional[str]):
        if title == None:
            return await ctx.send("Sorry! You forgot to add inputs! :open_mouth: Please provide some! :slight_smile:")
        if reaction == None or not emojis.check_emoji(reaction):
            return await ctx.send("Sorry! You have an invalid emoji! :cry: Please try again! :smile:")
        if rewards == None:
            return await ctx.send("Sorry! You have invalid rewards! :cry: Please try again! :smile:")
        giveaway_author = str(ctx.message.author)
        events_data = events.get_events_json()
        if not events.check_event(events_data, 'giveaways'):
            events_data['giveaways'] = {}
        if not giveaway_author in events_data['giveaways']:
            events_data['giveaways'][giveaway_author] = []
        rewards = rewards.strip("]['").split("', '")
        giveaway_json = {'title': title,
                         'reaction': reaction,
                         'start_time': datetime.now(),
                         'participants': {},
                         'rewards': rewards
                         }
        events_data['giveaways'][giveaway_author].append(giveaway_json)
        print(giveaway_json)

        # events.set_events_json(events_data)

        rewards_list = []
        count = 0
        for reward in rewards:
            count += 1
            rewards_list = rewards_list + \
                [f"{string_formatter.make_ordinal(count)} Place: **{reward}**"]
        # *********
        # | embed |
        # *********
        embed = Embed(title=f"{ctx.author.display_name}'s __{title}__ Giveaway!",
                      description=f"React with {reaction} to join the giveaway!",
                      colour=ctx.author.colour)
        # embed fields
        embed.add_field(name="Prizes:",
                        value='\n'.join(rewards_list), inline=False)
        embed.add_field(name="Description:",
                        value=description, inline=False)
        # embed footer
        embed.set_footer(
            text=f"Giveaway By: {giveaway_author}\n{reaction} Type \"BB endgiveaway {title}\" to end the giveaway!")
        msg = await ctx.send(embed=embed)
        await msg.add_reaction(reaction)


def setup(bot):
    bot.add_cog(giveawaymodule(bot))
