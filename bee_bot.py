# *********************************************************************************************************************
# bee_bot.py
# *********************************************************************************************************************

import os
import discord
import itertools

from discord.ext import commands, tasks
from dotenv import load_dotenv
from pretty_help import PrettyHelp

# get all cog extensions
all_extensions = [
    'cogs.admin.admin_beebot_reset_module',
    'cogs.admin.test_module',
    # 'cogs.beebot_profile.beebotprofilemodule',
    'cogs.events.eventsmodule',
    'cogs.games.league_of_legends.lolclashmodule',
    'cogs.games.league_of_legends.lolinfomodule',
    'cogs.games.league_of_legends.lolprofilemodule',
    'cogs.games.gamesmodule',
    # 'cogs.games.teamfight_tactics',
    'cogs.helper.listeners.reactions_listener',
    'cogs.music.musicmodule',
    'cogs.responses.responsesmodule'
]


def get_prefix(bot, message):
    prefixes = ['BB ', 'bb ', 'Bb ', 'bB ']  # BeeBot exclusive
    # prefixes = ['B ', 'b ']  # BeeBot-Testing exclusive
    return commands.when_mentioned_or(*prefixes)(bot, message)


# get from .env file
load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

# connecting with discord with "discord intents"
intents = discord.Intents.default()
intents.members = True

# bot setup
bot = commands.Bot(command_prefix=get_prefix, description='🐝 Hello! I am BeeBot! 🐝',
                   case_insensitive=True, intents=intents, help_command=PrettyHelp())

# load extensions(cogs) listed above in [all_extensions].
if __name__ == '__main__':
    for extension in all_extensions:
        bot.load_extension(extension)


@bot.event
async def on_ready():
    print('----------------------------------------------\n'
          f'Logged in as: {bot.user.name} - {bot.user.id}\nVersion: {discord.__version__}\n\n')
    await bot.change_presence(status=discord.Status.online)
    # starting task loops
    change_activity.start()
    print(f'BeeBot successfully logged in and booted! :D'
          '\n----------------------------------------------')


statuslist = itertools.cycle([
    'League of Legends [type \"BB help\"]',
    'with your Mom [type \"BB help\"]',
    'with BEES NUTS [type \"BB help\"]',
    'RealLife.exe [type \"BB help\"]',
    'myself :c [type \"BB help\"]',
    'with your Waifu [type \"BB help\"]',
    'with my Queen Bee [type \"BB help\"]',
    'literally nothing [type \"BB help\"]',
    'a prank [type \"BB help\"]'
])


# change activity
@tasks.loop(seconds=900)
async def change_activity():
    await bot.change_presence(activity=discord.Game(next(statuslist)))


bot.run(DISCORD_TOKEN, bot=True, reconnect=True)
