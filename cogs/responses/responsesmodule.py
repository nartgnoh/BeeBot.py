# *********************************************************************************************************************
# responsesmodule.py
# - bee_facts command
# - colour command
# - happy_birthday command
# - coin_flip command
# - dice_roll command
# - gif command
# *********************************************************************************************************************

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
admin_specific_command_name = 'Bot Admin'

# responsesmodule class


class responsesmodule(commands.Cog, name="ResponsesModule", description="beefacts, colour, happybirthday, coinflip, diceroll, gif"):
    def __init__(self, bot):
        self.bot = bot

    # *********************************************************************************************************************
    # bot command to show bee facts
    # *********************************************************************************************************************
    @commands.command(name='beefacts', aliases=['bee', 'beefact', 'fact', 'facts', '🐝'], help='🐝 Bee facts!')
    async def bee_facts(self, ctx):
        # get resources directory
        resources_directory = "/".join(
            list(current_directory.split('/')[0:-2])) + '/resource_files'
        # get image directory
        img_directory = resources_directory + '/image_files/bee_facts_images'
        bee_facts_images = random.choice([
            x for x in os.listdir(img_directory)
            if os.path.isfile(os.path.join(img_directory, x))
        ])
        # credits:
        # idea from https://github.com/SamKeathley/BeeBot
        # additional facts from https://www.sciencelearn.org.nz/resources/2002-bees-fun-facts
        with open(resources_directory + '/text_files/bee_facts.txt', 'r') as file:
            fact_quotes = file.readlines()
            fact_message = random.choice(fact_quotes)
        # *********
        # | embed |
        # *********
        embed = Embed(title=fact_message,
                      colour=discord.Colour.gold())
        # embed image
        file = discord.File(
            f'resource_files/image_files/bee_facts_images/{bee_facts_images}', filename="image.gif")
        embed.set_image(url='attachment://image.gif')
        # *************
        # | reactions |
        # *************
        msg = await ctx.send(file=file, embed=embed)
        await msg.add_reaction("🐝")

    # *********************************************************************************************************************
    # bot command to pick random colour
    # *********************************************************************************************************************
    @commands.command(name='pickcolour', aliases=['pickcolor', 'colour', 'color', '🎨'],
                      help='🎨 Picks a colour! [Typically chroma colours]')
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
    async def happy_birthday(self, ctx, *, member_name: Optional[str]):
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
        # *************
        # | reactions |
        # *************
        hbd_emojis = ["🎂", "🥳", "🎈", "🎁"]
        random.shuffle(hbd_emojis)
        for emoji in hbd_emojis:
            await msg.add_reaction(emoji)

    # *********************************************************************************************************************
    # bot command to flip coin
    # *********************************************************************************************************************
    @commands.command(name='coinflip', aliases=['coin', 'coins', 'flip', 'flips', '🟡'], help='🟡 Simulates coin flip. [Max coins: 100]')
    async def coin_flip(self, ctx, number_of_coins: Optional[int]):
        cf_results = ''
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
            await ctx.send('Sorry! Your number(s) are out of bounds! :cry: Try again! [Max dice: 100D100]')
        else:
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
        # *********
        # | embed |
        # *********
        embed = Embed(title=f'GIF from Tenor for \"{search}\"',
                      colour=discord.Colour.blue())
        # embed footer
        embed.set_footer(text=f'Reply to {ctx.author.display_name}',
                         icon_url=ctx.author.avatar_url)
        # make the search, url friendly by changing all spaces into "+"
        search.replace(' ', '+')
        # api.tenor website for given search
        # settings: ContentFilter = medium (PG)
        url = f'https://api.tenor.com/v1/search?q={search}&key={TENOR_KEY}&ContentFilter=medium'
        # get url info
        get_url_info = requests.get(url)
        # 404 status_code means tenor is not working/down
        if get_url_info.status_code == 404:
            await ctx.send("Sorry! Tenor is not working at the moment! :cry:")
        # 200 status_code means tenor is working
        elif get_url_info.status_code == 200:
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
                # embed gif
                embed.set_image(url=result_gif)
                await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(responsesmodule(bot))
