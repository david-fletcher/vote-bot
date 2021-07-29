# votebot.py
import os
import json
import discord
from discord.ext import commands
from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
BOT_USER_ID = -1
bot = commands.Bot(command_prefix='vb!')

def_up_emoji = '\U00002B06\U0000FE0F'
def_down_emoji = '\U00002B07\U0000FE0F'
server_data = {}


@bot.event
async def on_ready():
    # set globals
    global BOT_USER_ID, server_data
    BOT_USER_ID = bot.user.id
    print(f'{bot.user} has connected to Discord!')
    # read in former config
    read_config_from_file()

    # if we have been added to servers when we weren't active, set up their data
    for g in bot.guilds:
        if (str(g.id) not in server_data):
            init_new_guild(g)
    
    # save the config again
    write_config_to_file()


@bot.event
async def on_guild_join(guild):
    init_new_guild(guild)
    write_config_to_file()


@bot.event
async def on_message(message):
    global server_data
    # if a message is posted in a watched channel
    if (message.channel.id in server_data[str(message.guild.id)]['watching']):
        # add vote reactions
        await react_with_emoji(message)
        return

    # if the bot is mentioned by name in any channel
    if ((server_data[str(message.guild.id)]['vote_on_mention'] == True) and 
        (BOT_USER_ID in list(map(lambda u: u.id, message.mentions)))):
        # add vote reactions
        await react_with_emoji(message)
        return
    
    # if neither of the above are true, try to process the commands sent
    if ((server_data[str(message.guild.id)]['config_channel'] == None) or 
        (server_data[str(message.guild.id)]['config_channel']) == message.channel.id):
        await bot.process_commands(message)


@bot.command(
    help='Add a text channel from this server to the list of channels that will receive vote reactions on every message',
    brief='Add a text channel to the watch list'
)
async def watch(ctx, channel: discord.TextChannel):
    global server_data
    # ensure the channel isn't already present in the watch list
    if (channel.id in server_data[str(ctx.guild.id)]['watching']): 
        await ctx.send(f'{channel.mention} is already in the watch list.')
        return

    # add channel specified to watch list
    server_data[str(ctx.guild.id)]['watching'].append(channel.id)
    await ctx.send(f'Added {channel.mention} to the watch list.')

    write_config_to_file()


@bot.command(
    help='Remove a text channel from the list of channels that will receive vote reactions on every message',
    brief='Remove a text channel from the watch list'
)
async def unwatch(ctx, *, channel: discord.TextChannel):
    global server_data
    # ensure channel is present in watch list
    if (channel.id not in server_data[str(ctx.guild.id)]['watching']):
        await ctx.send(f'{channel.mention} was not in the watch list.')
        return
    
    # remove channel specified from watch list
    server_data[str(ctx.guild.id)]['watching'].remove(channel.id)
    await ctx.send(f'Removed {channel.mention} from the watch list.')

    write_config_to_file()


@bot.command(
    help='Show a list of all the server channels that will receive vote reactions on every message',
    brief='Show the list of text channels currently watched'
)
async def show(ctx):
    global server_data
    # get a list of TextChannel objects from the watch list
    ch_list = list(filter(lambda ch: ch.id in server_data[str(ctx.guild.id)]['watching'], ctx.guild.channels))

    if (len(ch_list) < 1): 
        await ctx.send('I am not currently watching any channels from this server.')
        return

    # build a list of channel mention objects and print a helpful message back to the user
    ch_name_list = '\n'.join(list(map(lambda ch: ch.mention, ch_list)))

    # determine what the current vote-on-mention setting is
    vom_setting = server_data[str(ctx.guild.id)]['vote_on_mention']
    vom_msg = "yes"
    if (vom_setting == False): vom_msg = "no"

    full_msg = ('I am currently watching the following from this server:\n'
                f'{ch_name_list}\n\n'
                f'The vote-on-mention option is currently configured to **{vom_msg}**.'
                )
    


    await ctx.send(full_msg)

@bot.command(
    help='Configure the bot to add vote reactions to messages in any channel that @ mentions the bot. Use "yes" or "no" as arguments.',
    brief='Option to add vote reactions to any messages with @VoteBot',
    name='vote-on-mention'
)
async def vote_on_mention(ctx, yesno):
    global server_data
    # determine user input
    if (yesno.lower() == 'yes'):
        server_data[str(ctx.guild.id)]['vote_on_mention'] = True
        await ctx.send('Changed vote-on-mention option to "yes".')
        write_config_to_file()
    elif (yesno.lower() == 'no'):
        server_data[str(ctx.guild.id)]['vote_on_mention'] = False
        await ctx.send('Changed vote-on-mention option to "no".')
        write_config_to_file()
    else: 
        await ctx.send('This command only accepts the words "yes" or "no".')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Missing required argument: `{}`'.format(error.param))
    elif isinstance(error, commands.BadArgument):
        await ctx.send('Could not parse commands argument; try typing `vb!help`.')
    elif isinstance(error, commands.CommandNotFound):
        await ctx.send('I do not recognize that command; try typing `vb!help`.')


async def react_with_emoji(message):
    global server_data
    await message.add_reaction(server_data[str(message.guild.id)]['emoji']['up'])
    await message.add_reaction(server_data[str(message.guild.id)]['emoji']['down'])


def read_config_from_file():
    global server_data
    try:
        with open('server.json', 'r') as file:
            server_data = json.load(file)
    except:
        print('error reading from file')
        server_data = {}


def write_config_to_file():
    global server_data
    try:
        with open('server.json', 'w') as file:
            json.dump(server_data, file)
    except:
        print('error writing to file')


def init_new_guild(guild):
    global server_data
    server_data[str(guild.id)] = {
        'watching': [],
        'config_channel': None,
        'vote_on_mention': False,
        'emoji': {
            'up': def_up_emoji,
            'down': def_down_emoji
        }
    }

# start running the bot
bot.run(TOKEN)