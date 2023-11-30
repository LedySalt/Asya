import os
import asyncio
from dotenv import load_dotenv

import discord
from discord.ext import commands
from discord.ext.commands import MissingPermissions
from discord.ext.commands import MissingRequiredArgument

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to the guild {GUILD}')


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.send(f'{ctx.author.name}, you dont have such rights')
    elif isinstance(error, MissingRequiredArgument):
        await ctx.send(f'{ctx.author.name}, you wrote nonsense')


@bot.command()
async def ping(ctx):
    await ctx.send('Hello, I am here')


@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, user: discord.Member, *, reason = ''):
    if user.guild_permissions.administrator:
        await ctx.send(f'{ctx.author.name} tried to kick the admin')
    else:
        await user.kick(reason=reason)
        await ctx.send(f'{user.name} was kicked: {reason}')



@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, user: discord.Member, *, reason = ''):
    if ctx.author == user:
        await ctx.send(f'You cannot ban yourself')
    elif user.guild_permissions.administrator:
        await ctx.send(f'{ctx.author.name} tried to ban the admin')
    else:
        await user.ban(reason=reason)
        await ctx.send(f'{user.name} was banned: {reason}')


@bot.command()
@commands.has_permissions(administrator=True)
async def unban(ctx, *, user):

    user = int(user[2:-1])

    banned_entry = [ban async for ban in ctx.guild.bans()]

    for ban_member in banned_entry:
        member = ban_member.user
        if (member.id == user):
            await ctx.guild.unban(member)
            await ctx.send(f'{member.name} was unbanned')
            return
    await ctx.send(f'Oops! This person is not on the ban list')




bot.run(TOKEN)
