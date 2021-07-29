from discord.ext import commands

from utils import read_config_from_file, write_config_to_file

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_ready(self):
        # set globals
        print(f'{self.bot.user} has connected to Discord!')
        # read in former config
        self.bot.server_data = read_config_from_file(self.bot.server_data)

        # if we have been added to servers when we weren't active, set up their data
        for g in self.bot.guilds:
            if (str(g.id) not in self.bot.server_data):
                self.init_new_guild(g)
        
        # save the config again
        write_config_to_file(self.bot.server_data)


    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        self.init_new_guild(guild)
        write_config_to_file(self.bot.server_data)


    @commands.Cog.listener()
    async def on_message(self, message):
        # if a message is posted in a watched channel
        if (message.channel.id in self.bot.server_data[str(message.guild.id)]['watching']):
            # add vote reactions
            await self.react_with_emoji(message)
            return

        # if the bot is mentioned by name in any channel
        if ((self.bot.server_data[str(message.guild.id)]['vote_on_mention'] == True) and 
            (self.bot.user.id in list(map(lambda u: u.id, message.mentions)))):
            # add vote reactions
            await self.react_with_emoji(message)
            return
        
        # if neither of the above are true, try to process the commands sent
        if ((self.bot.server_data[str(message.guild.id)]['config_channel'] == None) or 
            (self.bot.server_data[str(message.guild.id)]['config_channel']) == message.channel.id):
            await self.bot.process_commands(message)


    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Missing required argument: `{}`'.format(error.param))
        elif isinstance(error, commands.BadArgument):
            await ctx.send('Could not parse an argument; try typing `vb!help`.')
        elif isinstance(error, commands.CommandNotFound):
            await ctx.send('The bot does not recognize that command; try typing `vb!help`.')
        else:
            await ctx.send(error)


    async def react_with_emoji(self, message):
        # retrieve values; could be a unicode string or custom discord.Emoji ID (int)
        up_emoji = self.bot.server_data[str(message.guild.id)]['emoji']['up']
        down_emoji = self.bot.server_data[str(message.guild.id)]['emoji']['down']

        # if a discord.Emoji, retrieve the emoji representation
        if (isinstance(up_emoji, int)):
            up_emoji = self.bot.get_emoji(up_emoji)

        if (isinstance(down_emoji, int)):
            down_emoji = self.bot.get_emoji(down_emoji)

        # add reactions
        await message.add_reaction(up_emoji)
        await message.add_reaction(down_emoji)


    def init_new_guild(self, guild):
        self.bot.server_data[str(guild.id)] = {
            'watching': [],
            'config_channel': None,
            'vote_on_mention': False,
            'emoji': {
                'up': self.bot.def_up_emoji,
                'down': self.bot.def_down_emoji
            }
        }
