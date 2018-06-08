import sys
import os
import discord
from discord.ext import commands
import asyncio
import json
import botDeOuf
from utils import anti_capitalize


def check_versions():
    print("discord.py " + discord.__version__) #discord.py 1.0.0a needed (pip3 install -U git+https://github.com/Rapptz/discord.py@rewrite#egg=discord.py[voice])
    print("python" + sys.version) #python >= 3.5

def setup(config):
    try:
        os.stat(config["file"]["folder path"])
    except:
        os.mkdir(config["file"]["folder path"])

check_versions()

with open("./config.json", "r") as f:
    config = json.load(f)
    setup(config)
    bot = botDeOuf.BotDeOuf(config)

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
