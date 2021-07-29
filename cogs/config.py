import discord
from discord.ext import commands

from utils import write_config_to_file

class Config(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(
        help="Add or update the channel used to configure the bot. If set, the bot will only respond to configuration changes within the specified channel.",
        brief="Update bot to only be configurable in given channel.",
        name="upd-conf-channel"
    )
    async def update_config_channel(self, ctx, channel: discord.TextChannel):
        # update settings and save
        self.bot.server_data[str(ctx.guild.id)]['config_channel'] = channel.id
        await ctx.send(f'Updated bot configuration channel to {channel.mention}')

        write_config_to_file(self.bot.server_data)


    @commands.command(
        help="Clear the configuration channel option, allowing the bot to be configured in any channel.",
        brief="Clear exclusive bot configuration channel.",
        name="clr-conf-channel"
    )
    async def remove_config_channel(self, ctx):
        # update settings and save
        self.bot.server_data[str(ctx.guild.id)]['config_channel'] = None
        await ctx.send('Removed bot configuration channel. Bot is now configurable anywhere in the server.')

        write_config_to_file(self.bot.server_data)