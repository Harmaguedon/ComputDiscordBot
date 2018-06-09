import asyncio
import asyncpg
import discord
import inspect
import time
import sys
import dbManager
from datetime import datetime as dt
from discord.ext import commands
from utils import capitalize, lower

class BotDeOuf(commands.Bot):
    default_channels = []
    admins = None
    launch_time = None
    config = None
    db = None

    def __init__(self, config):
        self.config = config
        self.admins = self.config["bot"]["admins"]

        loop = asyncio.get_event_loop()
        self.db = loop.run_until_complete(dbManager.connection(self.db, self.config["bot"]["database config"]))
        loop.run_until_complete(dbManager.setup(self.db))

        super().__init__(command_prefix=self.config["bot"]["prefix"])
        self.remove_command("help")

    def run(self):
        super().run(self.config["bot"]["token"], reconnect=True)

    async def is_admin(self, ctx):
        if not (ctx.author.name+ctx.author.discriminator) in self.admins:
            await ctx.send("{} This command is restricted to admins users".format(ctx.author.mention))
            return False
        return True

    """send a message to all defaults channel"""
    async def send_message_default(self, message):
        for channel in self.default_channels:
            await channel.send(message)

    #Events-------------------------------------------------------------------------

    async def on_ready(self):
        self.launch_time = dt.utcnow()
        for guild_name, channel_name in (self.config["bot"]["default channels"]).items():
            guild = discord.utils.get(self.guilds, name=guild_name)
            if guild != None:
                channel = discord.utils.get(guild.channels, name=channel_name)
                if channel != None:
                    self.default_channels.append(channel)
        await self.send_message_default(self.config["bot"]["connection message"])

        for extension in self.config["bot"]["startup extensions"]:
            try:
                self.load_extension(extension)
            except Exception as e:
                exc = '{}: {}'.format(type(e).__name__, e)
                print('Failed to load extension {}\n{}'.format(extension, exc))
        print('Bot ready!')
        print('Logged in as ' + self.user.name)
        print('-------')
