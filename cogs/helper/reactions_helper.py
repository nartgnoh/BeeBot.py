# *********************************************************************************************************************
# reactions_helper.py
# - Uses on_raw_reaction_add to see all reactions
# *********************************************************************************************************************

from discord.ext.commands import Cog


class reactions_helper(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.polls = []
        self.giveaways = []

    @Cog.listener()
    async def on_raw_reaction_add(self, payload):
        # *********************************************************************************************************************
        # giveaway
        # *********************************************************************************************************************
        print("hello")



def setup(bot):
    bot.add_cog(reactions_helper(bot))
