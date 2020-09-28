import sys

import discord
from discord.ext import commands

from config import Config
from work_with_vk_api import PostFetcher


config = Config()
token = config.bot_token
prefix = config.bot_prefix
startup_extensions = ['PostHandler', 'SettingsEditor']

if not token or not prefix:
    print("Are you sure, that you set command prefix and Discord bot token in the config.ini?")
    sys.exit()

client = commands.Bot(command_prefix = prefix)
client.remove_command('help')

@client.event
async def on_command_error(ctx, error):
    print(f'\nCommand Error\nGuild:{ctx.guild.name}\nChannel:{ctx.channel.name}')
    print(f'{ctx.author.name}({ctx.author.id}) has tried to improperly use a command.')
    print(f'The error: {error}\n')

@client.event
async def on_ready():
    await client.change_presence(activity = discord.Activity(type = discord.ActivityType.watching, name = 'Your beatiful face'))
    print(f'{client.user.name} is ready.')

if __name__ == '__main__':

    for extension in startup_extensions:
        try:
            client.load_extension(f'cogs.{extension}')
        except Exception as e:
            print(f'Failed to load extension: {extension}')
            print(f'\tError:{e}')
            continue
        print(f'Successfully loaded extension: {extension}')

    client.run(token)
