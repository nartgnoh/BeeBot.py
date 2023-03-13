# *********************************************************************************************************************
# admin_beebot_reset_module.py
# - admin_beebot_reset_all_events command
# - admin_beebot_reset_all_urls command (wip)
# - admin_beebot_reset_all_beebot_profiles command
# - ADMIN_BEEBOT_RESET_ALL_BEEBOT_FILES command (wip)
# *********************************************************************************************************************

import os
import discord
import cogs.helper.helper_functions.events as events
import cogs.helper.helper_functions.games as games
import cogs.helper.helper_functions.beebot_profiles as beebot_profiles
import cogs.helper.helper_functions.urls as urls

from discord.ext import commands
from discord import Embed
from typing import Optional
from datetime import datetime

# role specific names
role_specific_command_name = 'Bot Commander'
admin_specific_command_name = 'Bot Admin'

# admin_beebot_reset_module class


class admin_beebot_reset_module(commands.Cog, name="Admin_BeeBot_Reset_Module",
                                description="Type \"BB help Admin_BeeBot_Reset_Module\" for options"):
    def __init__(self, bot):
        self.bot = bot

    # *********************************************************************************************************************
    # bot command admin beebot reset events
    # *********************************************************************************************************************
    @commands.command(name='admin_beebot_reset_events',
                      help='🛡️ Reset BeeBot events file. [Admin Specific]\n\nOptions: "all", "clash", "giveaways"')
    # only specific roles can use this command
    @commands.has_role(admin_specific_command_name)
    async def admin_beebot_reset_all_events(self, ctx, *, event: Optional[str]):
        if event == None:
            return await ctx.send('Please add an event to reset!')
        if event.lower() == 'all':
            events.set_events_json({})
            return await ctx.send('Reset ALL BeeBot events file.')
        events_json = events.get_events_json()
        if not event.lower() in events_json:
            return await ctx.send('Your event doesn\'t exist!')
        events_json.pop(event.lower())
        events.set_events_json(events_json)
        await ctx.send(f'Reset {event} BeeBot events file.')

    # *********************************************************************************************************************
    # bot command admin beebot reset games
    # *********************************************************************************************************************
    @commands.command(name='admin_beebot_reset_games',
                      help='🛡️ Reset BeeBot games file. [Admin Specific]\n\nOptions: "all", "blackjack"')
    # only specific roles can use this command
    @commands.has_role(admin_specific_command_name)
    async def admin_beebot_reset_all_games(self, ctx, *, game: Optional[str]):
        if game == None:
            return await ctx.send('Please add a game to reset!')
        if game.lower() == 'all':
            games.set_games_json({})
            return await ctx.send('Reset ALL BeeBot games file.')
        games_json = games.get_games_json()
        if not game.lower() in games_json:
            return await ctx.send('Your game doesn\'t exist!')
        games_json.pop(game.lower())
        games.set_games_json(games_json)
        await ctx.send(f'Reset {game} BeeBot games file.')

    # *********************************************************************************************************************
    # bot command admin beebot reset beebot profiles
    # *********************************************************************************************************************
    @commands.command(name='admin_beebot_reset_beebot_profiles', help='🛡️ Reset BeeBot profiles file. [Admin Specific]\n\n'
                      'Options: "user_id" (Example: "BeeBot#4676")')
    # only specific roles can use this command
    @commands.has_role(admin_specific_command_name)
    async def admin_beebot_reset_all_beebot_profiles(self, ctx, *, profile: Optional[str]):
        if profile == None:
            return await ctx.send('Please add a profile to reset!')
        # if profile.lower() == 'all':
        #     beebot_profiles.set_beebot_profiles_json({})
        #     return await ctx.send('Reset ALL BeeBot profile file.')
        profile_json = beebot_profiles.get_beebot_profiles_json()
        if not profile in profile_json:
            return await ctx.send(f'{profile} isn\'t on file!')
        profile_json.pop(profile)
        beebot_profiles.set_beebot_profiles_json(profile_json)
        await ctx.send(f'Removed {profile} in BeeBot profiles file.')

    # *********************************************************************************************************************
    # bot command admin beebot reset urls
    # *********************************************************************************************************************
    @commands.command(name='admin_beebot_reset_all_urls', help='🛡️ Reset BeeBot urls file. [Admin Specific]')
    # only specific roles can use this command
    @commands.has_role(admin_specific_command_name)
    async def admin_beebot_reset_all_urls(self, ctx):
        urls.set_urls_json({})
        await ctx.send('Reset BeeBot urls file.')

    # # *********************************************************************************************************************
    # # bot command admin beebot reset ALL BEEBOT FILES
    # # *********************************************************************************************************************
    # @commands.command(name='(CAUTION)ADMIN_BEEBOT_RESET_ALL_BEEBOT_FILES', help='🛡️ Reset BeeBot ALL BEEBOT FILES. [Admin Specific]')
    # # only specific roles can use this command
    # @commands.has_role(admin_specific_command_name)
    # async def ADMIN_BEEBOT_RESET_ALL_BEEBOT_FILES(self, ctx):
    #     await ctx.send('BB admin_beebot_reset_all_beebot_profiles')
    #     await ctx.send('BB admin_beebot_reset_all_events')


def setup(bot):
    bot.add_cog(admin_beebot_reset_module(bot))
