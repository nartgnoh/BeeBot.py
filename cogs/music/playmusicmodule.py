# *********************************************************************************************************************
# playmusicmodule.py
# - play
# - leave
# *********************************************************************************************************************

from dis import disco
import os
import discord
import cogs.helper.helper_functions.music as music_helper

from discord.ext import commands
from discord.voice_client import VoiceClient
from discord import Embed
from typing import Optional

# role specific names
role_specific_command_name = 'Bot Commander'
admin_specific_command_name = 'Bot Admin'

# playmusicmodule class


class playmusicmodule(commands.Cog, name="PlayMusicModule", description=""):
    def __init__(self, bot):
        self.bot = bot

    # *********************************************************************************************************************
    # bot command to play Youtube Audio
    # *********************************************************************************************************************
    @commands.command(name='play', aliases=['playaudio', 'playsong', '▶️'],
                      help='▶️ Plays YouTube audio! Provide YouTube search or link! [Max length: 15mins, Role specific]')
    # only specific roles can use this command
    @commands.has_role(role_specific_command_name)
    async def play(self, ctx, *, yt_search_or_link: Optional[str]):
        if yt_search_or_link == None:
            await ctx.send('Please provide a YouTube link or YouTube search info! :pleading_face:')
        else:
            if ctx.author.voice is None:
                await ctx.send('Please join a discord channel! :slight_smile:')
            else:
                check = music_helper.add_url(yt_search_or_link)
                if not check:
                    await ctx.send('Sorry! The song you were trying to play is too long! :cry: [Max length: 15mins]')
                else:
                    channel = ctx.message.author.voice.channel
                    voice = ctx.voice_client
                    if voice is None:
                        await channel.connect(timeout=300)
                    else:
                        await voice.move_to(channel)
                    voice = ctx.voice_client
                    if voice.is_playing():
                        await ctx.send(':musical_score: Your audio has been added to the queue! :musical_score:')
                    else:
                        current_song = music_helper.get_current_song()
                        music_helper.play_music(ctx)
                        # *********
                        # | embed |
                        # *********
                        embed = Embed(title=f"🎵 Now Playing 🎵\n{current_song['title']}",
                                    description=f"By: {current_song['channel']}\nDuration: {current_song['duration']}",
                                    colour=ctx.author.colour)
                        # embed thumbnail
                        thumb_url = current_song['thumbnails'][0]
                        embed.set_thumbnail(url=thumb_url)
                        await ctx.send(embed=embed)

    # # bot command to go to next audio in queue by reaction vote
    # @bot.command(name='next', aliases=['skip'], help='⏭️ Play the next audio! (Role specific) ♫')
    # # only specific roles can use this command
    # @commands.has_role(role_specific_command_name)
    # async def next(ctx):
    #     try:
    #         voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    #         # check if the queue is empty
    #         fl_check = Path(r'{}/resource_files/music_bot_files/yt_links.txt'.format(parent_dir))
    #         if not fl_check.stat().st_size == 0:
    #             # check if voice is playing
    #             if not voice.is_playing:
    #                 await ctx.send('Not playing any music right now. :thinking:')
    #             else:
    #                 # get url for message
    #                 url = get_url()
    #                 await ctx.send(':musical_note: BeeBot will now bee playing ***{}!*** '
    #                             ':musical_note:'.format(message_now_playing(url)))
    #                 # stop the current song
    #                 voice.stop()
    #                 # download "next_song.mp3" and play that
    #                 download_next_song(ctx)
    #         else:
    #             await ctx.send(
    #                 "There is not more audio in the queue! :flushed: Try the \"play\" command to add a song! :smile:")
    #     except:
    #         await ctx.send("An error has occurred! :open_mouth: Please try again!")

    # # bot command to pause audio
    # @bot.command(name='pause', aliases=['pauseaudio'], help='⏸️ Pause current audio playing! (Role specific) ♫')
    # # only specific roles can use this command
    # @commands.has_role(role_specific_command_name)
    # async def pause(ctx):
    #     voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    #     if voice.is_playing():
    #         await ctx.send("Pausing audio! :pause_button:")
    #         voice.pause()
    #     else:
    #         await ctx.send("Currently no audio is playing. :thinking:")

    # # bot command to resume audio
    # @bot.command(name='resume', aliases=['resumeaudio'], help='⏯️ Resume current audio playing! (Role specific) ♫')
    # # only specific roles can use this command
    # @commands.has_role(role_specific_command_name)
    # async def resume(ctx):
    #     voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    #     if voice.is_paused():
    #         await ctx.send("Resuming audio! :headphones:")
    #         voice.resume()
    #     else:
    #         await ctx.send("The audio is not paused. :thinking:")

    # *********************************************************************************************************************
    # bot command to leave voice channel and deletes queue
    # *********************************************************************************************************************

    @commands.command(name='leave', aliases=['stopaudio', 'leavecall', 'deletequeue', 'disconnect', '🔈'],
                      help='🔈 Beebot leaves voice channel and deletes current queue. [Role specific]')
    # only specific roles can use this command
    @commands.has_role(role_specific_command_name)
    async def leave(self, ctx):
        try:
            voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
            if voice.is_connected():
                voice.stop()
                music_helper.reset_songs_list()
                server = ctx.message.guild.voice_client
                await server.disconnect()
                await ctx.send("Ok I'll leave. :cry:")
        except:
            await ctx.send("BeeBot is not connected to a voice channel. :thinking:")


def setup(bot):
    bot.add_cog(playmusicmodule(bot))
