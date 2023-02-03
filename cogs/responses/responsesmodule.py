# *********************************************************************************************************************
# responsesmodule.py
# - bee_facts command
# - colour command
# - happy_birthday command
# - gif command
# *********************************************************************************************************************

import os
import discord
import random
import requests
import json
import openai

from discord.ext import commands
from discord import Embed
from typing import Optional
from dadjokes import Dadjoke
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


class responsesmodule(commands.Cog, name="ResponsesModule",
                      description="angry, beefacts, dadjoke, gif, happy, happybirthday, pickcolour, question, sad"):
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
    # bot command to show cute happy pictures
    # *********************************************************************************************************************
    @commands.command(name='happy', aliases=['c:', '😊'], help='😊 BeeBot happy! c:')
    async def happy(self, ctx):
        # get happy_images directory
        img_directory = "/".join(list(current_directory.split('/')
                                 [0:-2])) + '/resource_files/image_files/happy_images'
        happy_images = random.choice([
            x for x in os.listdir(img_directory)
            if os.path.isfile(os.path.join(img_directory, x))
        ])
        happy_quotes = [
            'Smiley! :smile:',
            'I\'m a happy bee! :smile:',
            'Very happy. c:'
        ]
        happy_message = random.choice(happy_quotes)
        # *********
        # | embed |
        # *********
        embed = Embed(title=happy_message,
                      colour=discord.Colour.gold())
        # embed image
        file = discord.File(
            f'resource_files/image_files/happy_images/{happy_images}', filename="image.gif")
        embed.set_image(url='attachment://image.gif')
        # *************
        # | reactions |
        # *************
        msg = await ctx.send(file=file, embed=embed)
        await msg.add_reaction("😊")

    # *********************************************************************************************************************
    # bot command to show cute sad pictures
    # *********************************************************************************************************************
    @commands.command(name='sad', aliases=['sadge', ':c', '😔'], help='😔 BeeBot sad! :c')
    async def sad(self, ctx):
        # get sad_images directory
        img_directory = "/".join(list(current_directory.split('/')
                                 [0:-2])) + '/resource_files/image_files/sad_images'
        sad_images = random.choice([
            x for x in os.listdir(img_directory)
            if os.path.isfile(os.path.join(img_directory, x))
        ])
        sad_quotes = [
            'Big sad.',
            'Big sadge.',
            'Do not talk me. Am sad.',
            'No talk me. Im sad.',
            'How could you?',
        ]
        sad_message = random.choice(sad_quotes)
        # *********
        # | embed |
        # *********
        embed = Embed(title=sad_message,
                      colour=discord.Colour.dark_blue())
        # embed image
        file = discord.File(
            f'resource_files/image_files/sad_images/{sad_images}', filename="image.gif")
        embed.set_image(url='attachment://image.gif')
        # *************
        # | reactions |
        # *************
        msg = await ctx.send(file=file, embed=embed)
        await msg.add_reaction("😔")

    # *********************************************************************************************************************
    # bot command to show cute angry pictures
    # *********************************************************************************************************************
    @commands.command(name='angry', aliases=['angy', 'mad', 'hmph', '>:c', 'madge', '😡'], help='😡 BeeBot angry! >:c')
    async def angry(self, ctx):
        # get angry_images directory
        img_directory = "/".join(list(current_directory.split('/')
                                 [0:-2])) + '/resource_files/image_files/angry_images'
        angry_images = random.choice([
            x for x in os.listdir(img_directory)
            if os.path.isfile(os.path.join(img_directory, x))
        ])
        angry_quotes = [
            'Do not talk me. Am anger.',
            'No talk me. Im angy.',
            'Wat you looking at?',
            'How dare you.',
            'Hmph.',
            'I will attack.',
            'I\'m so done.',
            ':angry:'
        ]
        angry_message = random.choice(angry_quotes)
        # *********
        # | embed |
        # *********
        embed = Embed(title=angry_message,
                      colour=discord.Colour.red())
        # embed image
        file = discord.File(
            f'resource_files/image_files/angry_images/{angry_images}', filename="image.gif")
        embed.set_image(url='attachment://image.gif')
        # *************
        # | reactions |
        # *************
        msg = await ctx.send(file=file, embed=embed)
        await msg.add_reaction("😡")

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
    # bot command tell a dad joke
    # *********************************************************************************************************************
    @commands.command(name='dadjoke', aliases=['joke', 'dadjokes', '🃏'],
                      help='🃏 Tells a dad joke!')
    async def dad_joke(self, ctx):
        await ctx.send(f"{Dadjoke().joke}  :rofl:")

    # *********************************************************************************************************************
    # bot command question
    # *********************************************************************************************************************
    @commands.command(name='question', aliases=['ask', '?', '❓'],
                      help='❓ Ask BeeBot a question!')
    async def question(self, ctx, *, question: Optional[str]):
        if question == None:
            return await ctx.send("Please ask me a question! :smile:")
        else:
            openai.api_key = os.getenv('OPENAI_KEY')
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=question,
                temperature=0.69,
                max_tokens=256,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
                )
            await ctx.send(response.choices[0].text)

    # *********************************************************************************************************************
    # bot command to send gif/tenor
    # *********************************************************************************************************************
    @commands.command(name='gif', aliases=['giphy', 'tenor', '😂'], help='😂 Random gif from Tenor. [Auto: bees]')
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
            return await ctx.send("Sorry! Tenor is not working at the moment! :cry:")
        # 200 status_code means tenor is working
        elif get_url_info.status_code == 200:
            # checking for results
            json_search = get_url_info.json()
            json_check = json_search['next']
            if json_check == "0":
                return await ctx.send(f"Sorry! Couldn't find any gifs for {search}! :cry:")
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
