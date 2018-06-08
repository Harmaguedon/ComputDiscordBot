import asyncio
import discord
import inspect
import sys
import json
from datetime import datetime as dt
from discord.ext import commands
from utils import capitalize, lower

class BotDeOuf(commands.Bot):
    default_channels = []
    admins = None
    launch_time = None
    config = None

    def __init__(self):
        with open("./config.json", "r") as f:
            self.config = json.load(f)

        self.admins = self.config["bot"]["admins"]

        super().__init__(command_prefix=self.config["bot"]["prefix"])
        self.remove_command("help")

    def run(self):
        #super().run("NDUxMDQzNzIzNzU3NzQ4MjI0.De8Fbw.A-ipYP4HFYKcw3FGCd_zqXmK6Qs") #Bot_portier
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
        asyncio.ensure_future(self.send_message_default(self.config["bot"]["connection message"]))

        for extension in self.config["bot"]["startup extensions"]:
            try:
                self.load_extension(extension)
            except Exception as e:
                exc = '{}: {}'.format(type(e).__name__, e)
                print('Failed to load extension {}\n{}'.format(extension, exc))

        print('Bot ready!')
        print('Logged in as ' + self.user.name)
        print('-------')
