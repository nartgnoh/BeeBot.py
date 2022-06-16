# bee_bot.py
import os
import discord
import sys, traceback

from discord.ext import commands
from dotenv import load_dotenv

# get all cog extensions
all_extensions = ['cogs.reactions.emotions',
                'cogs.reactions.reactions']

# get from .env file
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
TENOR_KEY = os.getenv('TENOR_KEY')
role_specific_command_name = 'Bot Commander'
owner_specific_command_name = 'Server Owner'

# connecting with discord with "discord intents"
intents = discord.Intents.default()
intents.members = True

# setup bot
bot = commands.Bot(command_prefix="BB ", description='Hello! I am BeeBot! c:', case_insensitive=True, intents=intents)

# load extensions(cogs) listed above in [all_extensions].
if __name__ == '__main__':
    for extension in all_extensions:
        bot.load_extension(extension)

@bot.event
async def on_ready():
    print(f'\n\nLogged in as: {bot.user.name} - {bot.user.id}\nVersion: {discord.__version__}\n')

    await bot.change_presence(status=discord.Status.online, activity=discord.Game(name="with BEES NUTS c: (type \"BB help\")"))
    print(f'BeeBot successfully logged in and booted! c:')


bot.run(TOKEN, bot=True, reconnect=True)