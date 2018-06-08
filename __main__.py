import sys
import discord
from discord.ext import commands
import asyncio
import botDeOuf
from utils import anti_capitalize

#multiping needed for netInfo

print("discord.py " + discord.__version__) #discord.py 1.0.0a needed (pip3 install -U git+https://github.com/Rapptz/discord.py@rewrite#egg=discord.py[voice])
print("python" + sys.version) #python >= 3.5

bot = botDeOuf.BotDeOuf()

@bot.command(name='load', pass_context=True)
@commands.check(bot.is_admin)
async def command_load(ctx, extension_name:anti_capitalize):
    """Loads an extension."""
    if not extension_name:
        await ctx.send("You have to specify the extension name")
        return
    try:
        bot.load_extension(extension_name)
    except (AttributeError, ImportError) as e:
        await ctx.send("```py\n{}: {}\n```".format(type(e).__name__, str(e)))
        return
    await ctx.send("{} loaded.".format(extension_name))

@bot.command(name='unload', pass_context=True)
@commands.check(bot.is_admin)
async def command_unload(ctx, extension_name:anti_capitalize):
    """Unloads an extension."""
    if not extension_name:
        await ctx.send("You have to specify the extension name")
        return
    bot.unload_extension(extension_name)
    await ctx.send("{} unloaded.".format(extension_name))

@bot.command(name='reload', pass_context=True)
@commands.check(bot.is_admin)
async def command_reload(ctx, extension_name:anti_capitalize):
    """reload an extension"""
    if not extension_name:
        await ctx.send("You have to specify the extension name")
        return
    bot.unload_extension(extension_name)
    try:
        bot.load_extension(extension_name)
    except (AttributeError, ImportError) as e:
        await ctx.send("```py\n{}: {}\n```".format(type(e).__name__, str(e)))
        return
    await ctx.send("{} reloaded.".format(extension_name))

bot.run()
