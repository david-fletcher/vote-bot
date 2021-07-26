# votebot.py
import os

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

up_emoji = '\U00002B06\U0000FE0F'
down_emoji = '\U00002B07\U0000FE0F'

watch_list = []
bot_configure_channel = 'bot-stuff'

bot_help_string = ('VoteBot Help:\n'
                   f'**!vb watch <channel mention>**: Start adding {up_emoji} and {down_emoji} to every message\n'
                   f'**!vb unwatch <channel mention>**: Stop adding {up_emoji} and {down_emoji} to every message\n'
                   '**!vb help**: view this menu')

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    if (message.channel.name == bot_configure_channel):
        # bot commands
        cmd_words = message.content.split(' ')
        if (cmd_words[0] == '!vb' and len(cmd_words) > 1):
            if (cmd_words[1] == 'watch'):
                if (len(message.channel_mentions) > 1):
                    await message.channel.send('Please only configure one channel at a time.')
                if (len(message.channel_mentions) < 1):
                    await message.channel.send('You must link the channel to watch.')

                channel = message.channel_mentions[0]
                if (not channel):
                    await message.channel.send(f'Channel does not exist.')
                else:
                    watch_list.append(channel.id)
                    await message.channel.send(f'Added {channel.mention} to the watch list.')
                return

            if (cmd_words[1] == 'unwatch'):
                if (len(message.channel_mentions) > 1):
                    await message.channel.send('Please only configure one channel at a time.')
                    return
                if (len(message.channel_mentions) < 1):
                    await message.channel.send('You must link the channel to unwatch.')
                    return

                channel = message.channel_mentions[0]
                if (not channel):
                    await message.channel.send(f'Channel does not exist.')
                else:
                    watch_list.remove(channel.id)
                    await message.channel.send(f'Removed {channel.mention} from the watch list.')
                return
            
            if (cmd_words[1] == 'help'):
                await message.channel.send(bot_help_string)
                return

            await message.channel.send(f'I do not know how to {cmd_words[1]}')
            return

        if ((cmd_words[0] == '!vb') and (len(cmd_words) <= 1)):
            await message.channel.send(bot_help_string)

    if (message.channel.id in watch_list):
        # add vote reactions
        await message.add_reaction(up_emoji)
        await message.add_reaction(down_emoji)

client.run(TOKEN)