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
                   '**!vb show**: show a list of watched channels in this server\n'
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
                    return
                if (len(message.channel_mentions) < 1):
                    await message.channel.send('You must link a valid channel to watch.')
                    return

                channel = message.channel_mentions[0]
                if (not channel):
                    await message.channel.send(f'Channel does not exist.')
                else:
                    if (channel.id in watch_list): 
                        await message.channel.send(f'{channel.mention} is already in the watch list.')
                        return

                    if (message.guild.id == channel.guild.id):
                        watch_list.append(channel.id)
                        await message.channel.send(f'Added {channel.mention} to the watch list.')
                    else:
                        await message.channel.send('You cannot add a channel from another server to the watch list!')
                return

            if (cmd_words[1] == 'unwatch'):
                if (len(message.channel_mentions) > 1):
                    await message.channel.send('Please only configure one channel at a time.')
                    return
                if (len(message.channel_mentions) < 1):
                    await message.channel.send('You must link a valid channel to unwatch.')
                    return

                channel = message.channel_mentions[0]
                if (not channel):
                    await message.channel.send(f'Channel does not exist.')
                else:
                    if (channel.id not in watch_list):
                        await message.channel.send(f'{channel.mention} was not in the watch list.')
                        return
                        
                    if (message.guild.id == channel.guild.id):
                        watch_list.remove(channel.id)
                        await message.channel.send(f'Removed {channel.mention} from the watch list.')
                    else:
                        await message.channel.send('You cannot unwatch a channel from a different server!')
                return

            if (cmd_words[1] == 'show'):
                ch_list = list(filter(lambda ch: ch.id in watch_list, message.guild.channels))

                if (len(ch_list) < 1): 
                    await message.channel.send('I am not currently watching any channels from this server.')
                    return

                ch_name_list = '\n'.join(list(map(lambda ch: ch.mention, ch_list)))
                ch_list_msg = ('I am currently watching the following from this server:\n'
                               f'{ch_name_list}'
                              )

                await message.channel.send(ch_list_msg)
                return
            
            if (cmd_words[1] == 'help'):
                await message.channel.send(bot_help_string)
                return

            await message.channel.send(f'I do not recognize this command: {cmd_words[1]}')
            return

        if ((cmd_words[0] == '!vb') and (len(cmd_words) <= 1)):
            await message.channel.send(bot_help_string)

    if (message.channel.id in watch_list):
        # add vote reactions
        await message.add_reaction(up_emoji)
        await message.add_reaction(down_emoji)

client.run(TOKEN)