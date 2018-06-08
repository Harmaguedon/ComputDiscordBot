import discord
from discord.ext import commands
from time import sleep
from threading import Thread
from random import randint
import asyncio
import socket

class Portier:
    """Door related commands"""

    bot = None
    sock = None
    thread_activity = None

    def __init__(self, bot):
        self.bot = bot
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (self.bot.config["portier"]["ip"], self.bot.config["portier"]["port"])
        self.sock.connect(server_address)
        self.bot.loop.create_task(self.activity_manager())

    def __unload(self):
        self.sock.close()

    def __del__(self):
        self.sock.close()

    async def activity_manager(self):
        while True:
            self.sock.sendall("door_state".encode('utf-8'))
            door_status = self.sock.recv(255).decode('utf-8')
            await self.bot.change_presence(activity=discord.Game(door_status))
            await asyncio.sleep(60) #1minute

    @commands.command(name='isOpen', pass_context=True)
    async def command_isOpen(self, ctx):
        """Display the door status"""
        self.sock.sendall("door_state".encode('utf-8'))
        await ctx.send(content = self.sock.recv(255).decode('utf-8'))

def setup(bot):
    bot.add_cog(Portier(bot))

def teardown(bot):
    pass
