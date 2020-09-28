import discord
from discord.ext import commands
from work_with_vk_api import PostFetcher
from config import Config

def setup(bot):
    bot.add_cog(PostHandler(bot))

class PostHandler(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def send_post(self, ctx, *args):
        config = Config()
        if not isinstance(ctx.message.channel, discord.channel.TextChannel):
            return
        if len(args) == 0:
            offset = 0
            try:
                vk_page_id = config.vk_page_id
            except KeyError:
                await ctx.send(f'Looks like you did not set VK page id in settings. You can do it by typing ``{self.bot.command_prefix}set vk_page your_id``')
                return
        elif len(args) == 1:
            offset = args[0]
            try:
                int(offset)
            except ValueError:
                await ctx.send('Looks like post number that you specified is incorrect!')
                return
            else:
                offset = int(offset) - 1

            try:
                vk_page_id = config.vk_page_id
            except KeyError:
                await ctx.send(f'Looks like you did not set VK page id in settings. You can do it by typing ``{self.bot.command_prefix}set vk_page your_id``')
                return
        elif len(args) == 2:
            offset = args[0]
            try:
                int(offset)
            except ValueError:
                await ctx.send('Looks like post number that you specified is incorrect!')
                return
            else:
                offset = int(offset) - 1
            vk_page_id = args[1]

        try:
            channel_id = config.notification_channel
        except KeyError:
            await ctx.send(f'Looks like you did not set channel in settings. You can do it by typing ``{self.bot.command_prefix}set channel #channel``')
            await ctx.send('Using current channel...')
            channel = ctx.channel
        else:
            channel = self.bot.get_channel(channel_id)
            if channel is None:
                await ctx.send(f'Looks like channel that had been set previously got deleted. You can do it again by typing ``{self.bot.command_prefix}set channel #channel``')
        try:
            role_id = config.notification_role
        except KeyError:
            await ctx.send(f'Looks like you did not set notification role in settings. You can do it by typing ``{self.bot.command_prefix}set role @role``')
            role = None
        else:
            role = ctx.guild.get_role(role_id)
            if role is None:
                await ctx.send(f'Looks like role that had been set previously got deleted. You can do it again by typing ``{self.bot.command_prefix}set role @role``')

        fetcher = PostFetcher(page_id=vk_page_id, vk_login = config.vk_credentials[0], vk_password = config.vk_credentials[1])
        try:
            post = fetcher.get_post(offset=offset)
        except:
            await ctx.send(f'Looks like I did not find any posts. Maybe I do not have enough permissions to see group\'s posts or there is no posts')
            return
        post_text = post[0]
        image_url = post[1]
        post_url = post[2]
        if post_text.find('\n'):
            text = post_text[:post_text.find('\n')]
        else:
            text = post_text
        text += f'\n``See full post:`` {post_url}'
        profile = fetcher.profile
        vk_embed = self.prepare_embed(text, image_url, profile.full_name, profile.avatar_url, 'vk')

        await ctx.send(content='Message preview:', embed=vk_embed)
        await ctx.send(f'Are you sure want to send this to {channel.name}?(yes/no)')
        def check(message):
            return ctx.author.id == message.author.id and (message.content.lower() == 'yes' or message.content.lower() == 'no')
        msg = await self.bot.wait_for('message', check=check)
        if msg.content.lower() == 'yes':
            if role is not None:
                await channel.send(content=f'{role.mention}', embed=vk_embed)
            else:
                await channel.send(embed=vk_embed)
            await ctx.send('Notification succesfully has been sent.')
        else:
            await ctx.send('Notification has been cancelled.')

    def prepare_embed(self, text, image_url, author_name, author_avatar_url, embed_type):
        embed = discord.Embed(description=text)
        if embed_type == 'vk':
            embed.set_author(name='VK Notification',
                icon_url='https://upload.wikimedia.org/wikipedia/commons/thumb/2/21/VK.com-logo.svg/1024px-VK.com-logo.svg.png')
            embed.color = discord.Color.blue()
        if image_url is not None:
            embed.set_image(url=image_url)
        embed.set_footer(text=author_name, icon_url=author_avatar_url)
        return embed
