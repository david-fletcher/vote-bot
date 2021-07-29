# votebot.py
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
BOT_USER_ID = -1
bot = commands.Bot(command_prefix='vb!')

up_emoji = '\U00002B06\U0000FE0F'
down_emoji = '\U00002B07\U0000FE0F'
watch_list = []


@bot.event
async def on_ready():
    global BOT_USER_ID
    BOT_USER_ID = bot.user.id
    print(f'{bot.user} has connected to Discord!')


@bot.event
async def on_guild_join(guild):
    return


@bot.event
async def on_message(message):
    # if a message is posted in a watched channel
    if (message.channel.id in watch_list):
        # add vote reactions
        await react_with_emoji(message)
        return

    # if the bot is mentioned by name in any channel
    if (BOT_USER_ID in list(map(lambda u: u.id, message.mentions))):
        # add vote reactions
        await react_with_emoji(message)
        return
    
    # if neither of the above are true, try to process the commands sent
    if (message.channel.name == 'bot-stuff'):
        await bot.process_commands(message)


@bot.command(
    help='Add a text channel from this server to the list of channels that will receive vote reactions on every message',
    brief='Add a text channel to the watch list'
)
async def watch(ctx, channel: discord.TextChannel):
    # ensure the channel isn't already present in the watch list
    if (channel.id in watch_list): 
        await ctx.send(f'{channel.mention} is already in the watch list.')
        return

    # add channel specified to watch list
    watch_list.append(channel.id)
    await ctx.send(f'Added {channel.mention} to the watch list.')


@bot.command(
    help='Remove a text channel from the list of channels that will receive vote reactions on every message',
    brief='Remove a text channel from the watch list'
)
async def unwatch(ctx, *, channel: discord.TextChannel):
    # ensure channel is present in watch list
    if (channel.id not in watch_list):
        await ctx.send(f'{channel.mention} was not in the watch list.')
        return
    
    # remove channel specified from watch list
    watch_list.remove(channel.id)
    await ctx.send(f'Removed {channel.mention} from the watch list.')


@bot.command(
    help='Show a list of all the server channels that will receive vote reactions on every message',
    brief='Show the list of text channels currently watched'
)
async def show(ctx):
    # get a list of TextChannel objects from the watch list
    ch_list = list(filter(lambda ch: ch.id in watch_list, ctx.guild.channels))

    if (len(ch_list) < 1): 
        await ctx.send('I am not currently watching any channels from this server.')
        return

    # build a list of channel mention objects and print a helpful message back to the user
    ch_name_list = '\n'.join(list(map(lambda ch: ch.mention, ch_list)))
    ch_list_msg = ('I am currently watching the following from this server:\n'
                    f'{ch_name_list}'
                  )

    await ctx.send(ch_list_msg)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Missing required argument: `{}`'.format(error.param))
    elif isinstance(error, commands.BadArgument):
        await ctx.send('Could not parse commands argument; try typing `vb!help`.')
    elif isinstance(error, commands.CommandNotFound):
        await ctx.send('I do not recognize that command; try typing `vb!help`.')


async def react_with_emoji(message):
    global up_emoji
    global down_emoji
    await message.add_reaction(up_emoji)
    await message.add_reaction(down_emoji)


def read_config_from_file():
    return


def write_config_to_file():
    return


def init_new_server():
    return

# start running the bot
bot.run(TOKEN)