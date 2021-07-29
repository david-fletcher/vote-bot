import discord
from discord.ext import commands

from utils import write_config_to_file

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(
        help='Add a text channel from this server to the list of channels that will receive vote reactions on every message',
        brief='Add a text channel to the watch list'
    )
    async def watch(self, ctx, channel: discord.TextChannel):
        # ensure the channel isn't already present in the watch list
        if (channel.id in self.bot.server_data[str(ctx.guild.id)]['watching']): 
            await ctx.send(f'{channel.mention} is already in the watch list.')
            return

        # add channel specified to watch list
        self.bot.server_data[str(ctx.guild.id)]['watching'].append(channel.id)
        await ctx.send(f'Added {channel.mention} to the watch list.')

        write_config_to_file(self.bot.server_data)


    @commands.command(
        help='Remove a text channel from the list of channels that will receive vote reactions on every message',
        brief='Remove a text channel from the watch list'
    )
    async def unwatch(self, ctx, channel: discord.TextChannel):
        # ensure channel is present in watch list
        if (channel.id not in self.bot.server_data[str(ctx.guild.id)]['watching']):
            await ctx.send(f'{channel.mention} was not in the watch list.')
            return
        
        # remove channel specified from watch list
        self.bot.server_data[str(ctx.guild.id)]['watching'].remove(channel.id)
        await ctx.send(f'Removed {channel.mention} from the watch list.')

        write_config_to_file(self.bot.server_data)


    @commands.command(
        help='Show a list of all the server channels that will receive vote reactions on every message',
        brief='Show the list of text channels currently watched'
    )
    async def show(self, ctx):
        # get a list of TextChannel objects from the watch list
        ch_list = list(filter(lambda ch: ch.id in self.bot.server_data[str(ctx.guild.id)]['watching'], ctx.guild.channels))

        if (len(ch_list) < 1): 
            await ctx.send('I am not currently watching any channels from this server.')
            return

        # build a list of channel mention objects and print a helpful message back to the user
        ch_name_list = '\n'.join(list(map(lambda ch: ch.mention, ch_list)))

        # determine what the current vote-on-mention setting is
        vom_setting = self.bot.server_data[str(ctx.guild.id)]['vote_on_mention']
        vom_msg = "yes"
        if (vom_setting == False): vom_msg = "no"

        # determine what the current config channel is
        config_msg = "any channel"
        if (not self.bot.server_data[str(ctx.guild.id)]['config_channel'] == None):
            config_msg = ctx.guild.get_channel(self.bot.server_data[str(ctx.guild.id)]['config_channel']).mention

        # determine emoji configuration
        # retrieve values; could be a unicode string or custom discord.Emoji ID (int)
        up_emoji = self.bot.server_data[str(ctx.guild.id)]['emoji']['up']
        down_emoji = self.bot.server_data[str(ctx.guild.id)]['emoji']['down']

        # if a discord.Emoji, retrieve the emoji representation
        if (isinstance(up_emoji, int)):
            up_emoji = self.bot.get_emoji(up_emoji)

        if (isinstance(down_emoji, int)):
            down_emoji = self.bot.get_emoji(down_emoji)

        full_msg = ('I am currently watching the following from this server:\n'
                    f'{ch_name_list}\n\n'
                    f'- The vote-on-mention option is currently configured to **{vom_msg}**.\n'
                    f'- The configuration channel is currently configured to **{config_msg}**.\n'
                    f'- The bot will use {up_emoji} for upvotes and {down_emoji} for downvotes.\n'
                    )

        await ctx.send(full_msg)