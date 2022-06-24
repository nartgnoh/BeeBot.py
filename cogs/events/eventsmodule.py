# *********************************************************************************************************************
# eventsmodule.py
# - giveaway command (wip)
# - polls command
# *********************************************************************************************************************

import os
import discord
import random
import cogs.helper.constants.emoji_constants as emoji_constants
import cogs.helper.helper_functions.emojis as emojis
import cogs.helper.helper_functions.events as events
import cogs.helper.helper_functions.string_formatter as string_formatter

from discord.ext import commands
from discord import Embed
from typing import Optional
from datetime import datetime

# role specific names
role_specific_command_name = 'Bot Commander'
admin_specific_command_name = 'Bot Admin'
giveaway_specific_command_name = 'Bot Giveaway Access'

# eventsmodule class


class eventsmodule(commands.Cog, name="EventsModule", description="polls"):
    def __init__(self, bot):
        self.bot = bot

    # *********************************************************************************************************************
    # bot command to make a poll in chat
    # *********************************************************************************************************************
    @commands.command(name='poll', aliases=['createpoll', 'makepoll', 'polls', '💈'],
                      help='💈 Make a poll! [Max options: 9, Questions and Options with spaces need quotes "", Role specific]\n\n'
                      'Example:\nBB poll "Who\'s excited for BeeBot\'s return?" Yes "Of course" Yay')
    # only specific roles can use this command
    @commands.has_role(role_specific_command_name)
    async def create_poll(self, ctx, question: Optional[str], *options):
        poll_hearts = emoji_constants.hearts()
        if question == None:
            return await ctx.send("Please add a question and option(s)! :slight_smile:")
        if len(options) == 0:
            return await ctx.send("Please add option(s)! :slight_smile:")
        elif len(options) > 9:
            return await ctx.send("Sorry! You have too many options! :cry: Please try again! [Max options: 9]")
        # *********
        # | embed |
        # *********
        embed = Embed(title="Polls",
                      description=question,
                      colour=ctx.author.colour)
        # embed footer
        embed.set_footer(
            text=f'Poll created by: {ctx.author.display_name}', icon_url=ctx.author.avatar_url)
        # embed fields
        fields = [("Options", "\n".join([f"{poll_hearts[idx]} {option}" for idx, option in enumerate(options)]), False),
                  ("Instructions", "React to cast a vote!", False)]
        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)
        # *************
        # | reactions |
        # *************
        msg = await ctx.send(embed=embed)
        for emoji in poll_hearts[:len(options)]:
            await msg.add_reaction(emoji)

    # *********************************************************************************************************************
    # bot command list active giveaways
    # *********************************************************************************************************************
    @commands.command(name='activegiveaways', aliases=['getgiveaways', 'listgiveaways', '💝'],
                      help='💝 Get a list of active giveaways!')
    # only specific roles can use this command
    @commands.has_role(role_specific_command_name)
    async def active_giveaways(self, ctx):
        events_data = events.get_events_json()
        if not 'giveaways' in events_data:
            return await ctx.send("Sorry! There are no active giveaways at the moment! :open_mouth:")
        if not events_data['giveaways']:
            return await ctx.send("Sorry! There are no active giveaways at the moment! :open_mouth:")
        for giveaway in events_data['giveaways']:
            message = await ctx.fetch_message(int(giveaway))
            await message.reply(f"**{events_data['giveaways'][giveaway]['title']}** run by **{events_data['giveaways'][giveaway]['giveaway_author_display_name']}**")

    # *********************************************************************************************************************
    # bot command to make a giveaway in chat
    # *********************************************************************************************************************
    @commands.command(name='giveaway', aliases=['creategiveaway', 'makegiveaway', '🎁'],
                      help='🎁 Make a giveaway! [Type "BB help giveaway" for more info, Role specific]\n\n'
                      'Titles with spaces need quotes "".\n'
                      'Prizes must be in a list format in apostrophes \'\' in descending order inside quotes "".\n'
                      'Example:\nBB giveaway "BB Bucks" 💵 "[\'500 BB Bucks\', \'200 BB Bucks\', \'100 BB Bucks\']"\nRules: Be good c:')
    # only specific roles can use this command
    @commands.has_role(giveaway_specific_command_name)
    async def create_giveaway(self, ctx, title: Optional[str], reaction: Optional[str],
                              rewards: Optional[str], *, description: Optional[str]):
        if title == None:
            return await ctx.send("Sorry! You forgot to add inputs! :open_mouth: Please provide some! :slight_smile:")
        if reaction == None or not emojis.check_emoji(reaction):
            return await ctx.send("Sorry! You have an invalid emoji! :cry: Please try again! :smile:")
        if rewards == None:
            return await ctx.send("Sorry! You have invalid rewards! :cry: Please try again! :smile:")
        events_data = events.get_events_json()
        if not events.check_event(events_data, 'giveaways'):
            events_data['giveaways'] = {}
        rewards = rewards.strip("]['").split("', '")
        giveaway_json = {'giveaway_author': str(ctx.message.author),
                         'giveaway_author_display_name': str(ctx.message.author.display_name),
                         'title': title,
                         'reaction': reaction,
                         'start_time': datetime.timestamp(datetime.now()),
                         'participants': {},
                         'rewards': rewards
                         }
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
            text=f"Giveaway By: {str(ctx.message.author.display_name)}\n{reaction} Type \"BB endgiveaway {title}\" to end the giveaway!")
        msg = await ctx.send(embed=embed)
        await msg.add_reaction(reaction)
        giveaway_json['message_id'] = int(msg.id)
        events_data['giveaways'][int(msg.id)] = giveaway_json
        events.set_events_json(events_data)

    # *********************************************************************************************************************
    # bot command to end a giveaway in chat
    # *********************************************************************************************************************
    @commands.command(name='endgiveaway', aliases=['finishgiveaway', '🎉'],
                      help='🎉 End a giveaway you made!')
    # only specific roles can use this command
    @commands.has_role(giveaway_specific_command_name)
    async def end_giveaway(self, ctx, *, title: Optional[str]):
        if title == None:
            return await ctx.send("Sorry! You forgot to add your title! :open_mouth: Please try again! :slight_smile:")
        events_data = events.get_events_json()
        giveaway_check = False
        for giveaway in events_data['giveaways']:
            giveaway = events_data['giveaways'][giveaway]
            if giveaway['title'] == title and giveaway['giveaway_author'] == str(ctx.message.author):
                giveaway_check = True
                giveaway = giveaway
                break
        if not giveaway_check:
            return await ctx.send("Sorry! You don't have a giveaway active! :cry:")
        reaction = giveaway['reaction']
        days = datetime.now() - datetime.fromtimestamp(giveaway['start_time'])
        participants = giveaway['participants']
        rewards = giveaway['rewards']
        # remove giveaway
        events_data['giveaways'].pop(str(giveaway['message_id']))
        events.set_events_json(events_data)
        # get winners
        party_keys = list(participants.keys())
        random.shuffle(party_keys)
        try:
            winners_list = random.sample(party_keys, len(rewards))
        except:
            winners_list = party_keys
        rewards_list = []
        count = 0
        final_message = ''
        for reward in rewards:
            count += 1
            if count <= len(winners_list):
                rewards_list = rewards_list + \
                    [f"{string_formatter.make_ordinal(count)} Place: **{participants[winners_list[count-1]]}** ({reward})"]
                final_message = final_message + \
                    f"{string_formatter.make_ordinal(count)} Place: <@{winners_list[count-1]}>\n"
            else:
                rewards_list = rewards_list + \
                    [f"{string_formatter.make_ordinal(count)} Place: N/A ({reward})"]
                final_message = final_message + \
                    f"{string_formatter.make_ordinal(count)} Place: N/A\n"
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
            text=f"Giveaway By: {giveaway['giveaway_author_display_name']}\n{reaction} This giveaway lasted {days.days} day(s)!")
        await ctx.send(embed=embed)
        await ctx.send(final_message)


def setup(bot):
    bot.add_cog(eventsmodule(bot))
