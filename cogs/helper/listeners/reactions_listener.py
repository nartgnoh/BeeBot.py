# *********************************************************************************************************************
# reactions_listener.py
# *********************************************************************************************************************
from discord.ext.commands import Cog


class Reactions(Cog):
    def __init__(self, bot):
        self.bot = bot

    # *********************************************************************************************************************
    # listener for on_raw_reaction_add
    # *********************************************************************************************************************
    @Cog.listener()
    async def on_raw_reaction_add(self, payload):
        # ***********************************
        # | delete message on '❌' reaction |
        # ***********************************
        message = await self.bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
        first_reaction_users = await message.reactions[0].users().flatten()
        for u in first_reaction_users:
            if u.bot and len(first_reaction_users) > 1 and payload.emoji.name == '❌':
                await message.delete()
                break


def setup(bot):
    bot.add_cog(Reactions(bot))
