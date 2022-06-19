# *********************************************************************************************************************
# emotionsmodule.py
# - happy command
# - sad command
# - angry command
# *********************************************************************************************************************

import os
import discord
import random

from discord.ext import commands
from discord import Embed
from typing import Optional

# get current directory
current_directory = os.path.dirname(os.path.realpath(__file__))
# role specific names
role_specific_command_name = 'Bot Commander'
admin_specific_command_name = 'Bot Admin'

# emotionsmodule class


class emotionsmodule(commands.Cog, name="EmotionsModule", description="happy, sad, angry"):
    def __init__(self, bot):
        self.bot = bot

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


def setup(bot):
    bot.add_cog(emotionsmodule(bot))
