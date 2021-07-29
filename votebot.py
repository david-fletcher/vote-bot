# votebot.py
import os
from discord.ext import commands
from dotenv import load_dotenv
load_dotenv()

from cogs.general import General
from cogs.config import Config
from cogs.reactions import Reactions
from cogs.events import Events

TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='vb!')
bot.def_up_emoji = '\U00002B06\U0000FE0F'
bot.def_down_emoji = '\U00002B07\U0000FE0F'
bot.server_data = {}

bot.add_cog(General(bot))
bot.add_cog(Config(bot))
bot.add_cog(Reactions(bot))
bot.add_cog(Events(bot))

# we register this listener and then just pass
# because events.py has it's own on_message listener that
# will get called instead.
@bot.event
async def on_message(*message):
    pass

# start running the bot
bot.run(TOKEN)