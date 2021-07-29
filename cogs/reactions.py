import discord
from discord.ext import commands

from utils import write_config_to_file

class Reactions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(
        help='Configure the bot to add vote reactions to messages in any channel that @ mentions the bot. Use "yes" or "no" as arguments.',
        brief='Option to add vote reactions to any messages with @VoteBot',
        name='vote-on-mention'
    )
    async def vote_on_mention(self, ctx, yesno):
        # determine user input
        if (yesno.lower() == 'yes'):
            self.bot.server_data[str(ctx.guild.id)]['vote_on_mention'] = True
            await ctx.send('Changed vote-on-mention option to "yes".')
        elif (yesno.lower() == 'no'):
            self.bot.server_data[str(ctx.guild.id)]['vote_on_mention'] = False
            await ctx.send('Changed vote-on-mention option to "no".')
        else: 
            await ctx.send('This command only accepts the words "yes" or "no".')
            return
        
        write_config_to_file(self.bot.server_data)


    @commands.command(
        help="Enable the use of a custom server emoji to be the upvote or downvote symbol.",
        brief="Change a vote reaction to be a custom server emoji.",
        name="use-custom-emoji"
    )
    async def upd_custom_emoji(self, ctx, updown, emoji: discord.Emoji):
        updn = updown.lower()
        # make sure we're handling error scenarios
        if (updn != 'up') and (updn != 'down'):
            await ctx.send('The second argument must be either "up" or "down".')
            return
        
        if (not emoji.is_usable()):
            await ctx.send('The bot cannot use this emoji; please select a custom emoji (cannot be unicode-standard).')
            return

        # save custom emoji
        self.bot.server_data[str(ctx.guild.id)]['emoji'][updn] = emoji.id
        await ctx.send(f'The bot will now use {emoji} for {updn}votes.')

        write_config_to_file(self.bot.server_data)


    @commands.command(
        help="Remove any custom server emoji configuration and go back to the default.",
        brief="Remove custom server emoji; use default instead.",
        name="del-custom-emoji"
    )
    async def del_custom_emoji(self, ctx, updown):
        # check which emoji we are changing
        if (updown.lower() == 'up'):
            self.bot.server_data[str(ctx.guild.id)]['emoji']['up'] = self.bot.def_up_emoji
            await ctx.send(f'The bot will now use {self.bot.def_up_emoji} for upvotes.')
        elif (updown.lower() == 'down'):
            self.bot.server_data[str(ctx.guild.id)]['emoji']['down'] = self.bot.def_down_emoji
            await ctx.send(f'The bot will now use {self.bot.def_down_emoji} for downvotes.')
        else:
            await ctx.send('The second argument must be either "up" or "down".')
            return

        write_config_to_file(self.bot.server_data)