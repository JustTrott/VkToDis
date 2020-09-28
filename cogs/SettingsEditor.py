import discord
from discord.ext import commands

from config import Config
from work_with_vk_api import PostFetcher

def setup(bot):
    bot.add_cog(SettingsEditor(bot))

class SettingsEditor(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.allowed_settings = ['channel', 'vk_page', 'role']

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def set(self, ctx, *args):
        config = Config()
        if not isinstance(ctx.message.channel, discord.channel.TextChannel):
            return
        def check_vk_profile(vk_page_id):
            fetcher = PostFetcher(page_id=vk_page_id, vk_login = config.vk_credentials[0], vk_password = config.vk_credentials[1])
            fetcher.connect_to_vk()
            if fetcher.profile is None:
                return False
            else:
                return True
        if (len(args) != 2
            or args[0] not in self.allowed_settings
            or args[0] == 'channel' and len(ctx.message.channel_mentions) < 1
            or args[0] == 'vk_page' and not check_vk_profile(args[1])
            or args[0] == 'role' and len(ctx.message.role_mentions) < 1):
            await ctx.send(embed=self.prepare_error_embed(ctx))
            return
        setting = args[0]
        if setting == 'channel':
            value = ctx.message.channel_mentions[0].id
        elif setting == 'vk_page':
            value = args[1]
        elif setting == 'role':
            value = ctx.message.role_mentions[0].id
        config.set(setting, str(value))
        await ctx.send(f'{setting} has been succesfully changed!')

    def prepare_error_embed(self, ctx):
        command_error_embed=discord.Embed(title='Whoops, that\'s not quite right', description='Looks like you tried to improperly use a command\nHere\'s some command tips', color=discord.Color.dark_red())
        command_error_embed.add_field(name=f'{self.bot.command_prefix}set channel #channel', value=f'_Usage example:_``{self.bot.command_prefix}set channel #main-chat``', inline=False)
        command_error_embed.add_field(name=f'{self.bot.command_prefix}set role @role', value=f'_Usage example:_``{self.bot.command_prefix}set role @Notifications``', inline=False)
        command_error_embed.add_field(name=f'{self.bot.command_prefix}set vk_page page_id_or_name', value=f'_Usage example:_``{self.bot.command_prefix}set vk_page durov``', inline=False)
        return command_error_embed
