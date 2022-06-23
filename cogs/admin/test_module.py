# *********************************************************************************************************************
# test_module.py
# image_test command
# *********************************************************************************************************************

import os
import discord


from discord.ext import commands
from discord import Embed
from typing import Optional
import cogs.helper.api.league_of_legends_api as lol_api
import cogs.helper.helper_functions.images as images

# role specific names
role_specific_command_name = 'Bot Commander'
admin_specific_command_name = 'Bot Admin'

# test_module class


class test_module(commands.Cog, name="Test_Module",
                  description="Type \"BB help Test_Module\" for options"):
    def __init__(self, bot):
        self.bot = bot

    # *********************************************************************************************************************
    # bot command test
    # *********************************************************************************************************************
    @commands.command(name='imagetest')
    # only specific roles can use this command
    @commands.has_role(admin_specific_command_name)
    async def champ_lookup(self, ctx, champ1, champ2):
        # get current lol version for region
        champions_version = lol_api.get_version()['n']['champion']
        champ_list = lol_api.get_champion_list(champions_version)['data']

        lol_champion1 = lol_api.champion_string_formatting(champ1)
        lol_champion2 = lol_api.champion_string_formatting(champ2)

        image1_url = f'http://ddragon.leagueoflegends.com/cdn/{champions_version}/img/champion/{lol_champion1}.png'
        image2_url = f'http://ddragon.leagueoflegends.com/cdn/{champions_version}/img/champion/{lol_champion2}.png'

        image1 = images.get_image_by_url(image1_url)
        image2 = images.get_image_by_url(image2_url)

        images.merge_images_width_wise(image1, image2, images.get_image_path(
            'riot_images/spectator/new_image.png'))

        image1 = images.new_blank_image()
        image2 = images.get_image_by_url(image2_url)

        images.merge_images_width_wise(image1, image2, images.get_image_path(
            'riot_images/spectator/new_image2.png'))

        await ctx.send("images")


def setup(bot):
    bot.add_cog(test_module(bot))
