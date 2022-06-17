# reactions.py
import os
import discord
import random
import requests
import json

from discord.ext import commands
from discord import Embed
from typing import Optional
from dotenv import load_dotenv

# get tenor_key from .env file
load_dotenv()
TENOR_KEY = os.getenv('TENOR_KEY')

# get current directory
current_directory = os.path.dirname(os.path.realpath(__file__))
# role specific names
role_specific_command_name = 'Bot Commander'
owner_specific_command_name = 'Server Owner'

# reactions class
class reactions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # *********************************************************************************************************************
    # bot command to show bee facts
    # *********************************************************************************************************************
    @commands.command(name='beefacts', aliases=['beefact', 'fact', 'facts', '🐝'], help='🐝 Bee facts!')
    async def facts(self, ctx):
        # get resources directory
        resources_directory = "/".join(list(current_directory.split('/')[0:-2])) + '/resource_files'
        # get image directory
        img_directory = resources_directory + '/image_files/bee_facts_images'
        fact_images = random.choice([
            x for x in os.listdir(img_directory)
            if os.path.isfile(os.path.join(img_directory, x))
        ])
        # credits:
        # idea from https://github.com/SamKeathley/BeeBot
        # additional facts from https://www.sciencelearn.org.nz/resources/2002-bees-fun-facts
        with open(resources_directory + '/text_files/bee_facts.txt', 'r') as file:
            fact_quotes = file.readlines()
            fact_message = random.choice(fact_quotes)

        msg = await ctx.send(f'{fact_message}',
                    file=discord.File(f'resource_files/image_files/bee_facts_images/{fact_images}'))
        await msg.add_reaction("🐝")

    # *********************************************************************************************************************
    # bot command to pick random colour
    # *********************************************************************************************************************
    @commands.command(name='pickcolour', aliases=['pickcolor', 'colour', 'color', '🎨'],
                help='🎨 Picks a colour (typically chroma colours).')
    async def colour(self, ctx):
        colours_quotes = [
            'Red ❤️', 'Orange 🧡', 'Yellow 💛', 'Green 💚', 'Light Blue 🧊', 'Indigo 💙', 'Purple 💜', 
            'White 🤍', 'Black 🖤', 'Brown 🤎' 'Pink 💗', 'Rainbow 🌈']
        colours_message = random.choice(colours_quotes)
        await ctx.send(colours_message)

    # *********************************************************************************************************************
    # bot command to wish someone a Happy Birthday
    # *********************************************************************************************************************
    @commands.command(name='happybirthday', aliases=['hbd', 'birthday', '🎂'],
                help='🎂 Wishes someone a Happy Birthday! Try a mention!')
    async def hbd(self, ctx, *, member_name: Optional[str]):
        if member_name == None:
            member_name = ''
        else:
            member_name = ' ' + member_name
        hbd_quotes = [
            f'HAPPY BIRTHDAY{member_name}!!!!!  :partying_face: :birthday: :tada:',
            f'Wishing you a Happy Birthday{member_name}! :relieved: :birthday: :tada:',
            f'May all your birthday wishes come true{member_name} — except for the illegal ones! :birthday: :tada: :neutral_face:'
        ]
        hbd_message = random.choice(hbd_quotes)
        msg = await ctx.send(hbd_message)

        hbd_emojis = ["🎂", "🥳", "🎈", "🎁"]
        random.shuffle(hbd_emojis)
        for emoji in hbd_emojis:
            await msg.add_reaction(emoji)

    # *********************************************************************************************************************
    # bot command to flip coin
    # *********************************************************************************************************************
    @commands.command(name='coinflip', aliases=['coin', 'coins', 'flip', 'flips', '🟡'], help='🟡 Simulates coin flip. [Max coins: 100]')
    async def coin_flip(self, ctx, number_of_coins: Optional[int]):
        try:
            # empty message
            cf_message = ''
            # default 1 coin
            if number_of_coins == None:
                number_of_coins = 1
            if number_of_coins > 100 or number_of_coins < 1:
                await ctx.send('Sorry! Your number is out of bounds! :cry: Try again! [Max coins: 100]')
            else:
                coin_flip_ht = [
                    'Heads, ',
                    'Tails, '
                ]
                cf_quotes = [
                    'You coin flip(s) were:\n',
                    'Clink, spin, spin, clink:\n',
                    'Heads or Tails? :open_mouth:\n',
                    'I wish you good RNG :relieved:\n',
                    ':coin:\n'
                ]
                # add coin flips to string
                for i in range(number_of_coins):
                    cf_message = cf_message + random.choice(coin_flip_ht)
                await ctx.send(f'{random.choice(cf_quotes)}{cf_message[:-2]}')
        except:
            # if out of bounds of bot's capability
            await ctx.send('Sorry! The coin is broken. :cry: Try again!')

    # *********************************************************************************************************************
    # bot command to roll dice (no specification is an auto 1D6)
    # *********************************************************************************************************************
    @commands.command(name='rolldice', aliases=['diceroll', 'roll', 'dice', '🎲'],
                help='🎲 Simulates rolling dice. [Auto: 1D6, Max dice: 100D100]')
    async def roll(self, ctx, number_of_dice: Optional[int], number_of_sides: Optional[int]):
        try:
            # default 1D6 dice
            if number_of_dice == None:
                number_of_dice = 1
            if number_of_sides == None:
                number_of_sides = 6
            if number_of_dice > 100 or number_of_dice < 1 or number_of_sides > 100 or number_of_sides < 1:
                await ctx.send('Sorry! Your number(s) are out of bounds! :cry: Try again! [Max dice: 100D100]')
            else:
                dice = [
                    str(random.choice(range(1, number_of_sides + 1)))
                    for _ in range(number_of_dice)
                ]
                rd_quotes = [
                    'Your dice roll(s) were:\n',
                    'Clack, rattle, clatter:\n',
                    'Highroller?!? :open_mouth:\n',
                    'I wish you good RNG :relieved:\n',
                    ':game_die:\n',
                    ':skull: + :ice_cube:\n'
                ]
                rd_message = random.choice(rd_quotes)
                await ctx.send(f'{rd_message}' + ', '.join(dice))
        except:
            # if out of bounds of bot's capability
            await ctx.send('Sorry! The dice is broken. :cry: Try again! ')

    # *********************************************************************************************************************
    # bot command to send gif/tenor
    # *********************************************************************************************************************
    @commands.command(name='gif', aliases=['giphy', 'tenor', '😂'], help='😂 Random gif from Tenor. [Auto: bees, Role Specific]')
    # only specific roles can use this command
    @commands.has_role(role_specific_command_name)
    async def gif(self, ctx, *, search: Optional[str]):
        # search 'bees' if no given search
        if search == None:
            search = 'bees'
        # set discord.Embed colour to blue
        embed = discord.Embed(colour=discord.Colour.blue(), title=f'GIF from Tenor for \"{search}\"')
        # make the search, url friendly by changing all spaces into "+"
        search.replace(' ', '+')
        # api.tenor website for given search
        # settings: ContentFilter = medium (PG)
        url = f'https://api.tenor.com/v1/search?q={search}&key={TENOR_KEY}&ContentFilter=medium'
        # get url info
        get_url_info = requests.get(url)
        # 200 status_code means tenor is working
        if get_url_info.status_code == 200:
            # checking for results
            json_search = get_url_info.json()
            json_check = json_search['next']
            if json_check == "0":
                await ctx.send(f"Sorry! Couldn't find any gifs for {search}! :cry:")
            else:
                # load json to get url data
                data = json.loads(get_url_info.text)
                # random choice between 0 and min of "9 or len(data['results'])"
                gif_choice = random.randint(0, min(9, len(data['results'])))
                # get gif result
                result_gif = data['results'][gif_choice]['media'][0]['gif']['url']
                # embed gif and send
                embed.set_image(url=result_gif)
                await ctx.send(embed=embed)
        # 404 status_code means tenor is not working/down
        elif get_url_info.status_code == 404:
            await ctx.send("Sorry! Tenor is not working at the moment! :cry:")

def setup(bot):
    bot.add_cog(reactions(bot))