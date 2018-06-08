import discord
from discord.ext import commands
from datetime import datetime
from multiping import MultiPing
import asyncio

class NetInfo:
    """Network related commads"""
    bot = None

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='pingBot', pass_context=True)
    async def command_pingBot(self, ctx):
        """Display the bot ping"""
        recieved = datetime.utcnow()
        await ctx.send('Ping')
        replied = datetime.utcnow()
        diff = (replied - recieved)
        await ctx.send('Pong : {} ms'.format(diff.microseconds / 1000))

    @commands.command(name='ping', pass_context=True)
    async def command_ping(self, ctx):
        """Display the local network ping"""
        mp = MultiPing(["8.8.8.8","8.8.8.4"])
        responses = {}
        for i in range(3):
            mp.send()
            for i in range(50):
                rep, _ =mp.receive(0.1)
                if rep:
                    responses = rep
                    break
            if responses:
                break
        ip, time = responses.popitem()
        await ctx.send("Pong : {} ms".format(int(time*1000)))

    """@commands.command(name='vpnStatus', pass_context=True)
    async def command_vpnStatus(self, ctx)
        #essayer de ping la gateway vpn?
        try
            voice_channel = self.bot.voice_client_in(ctx.guild)
            voice_client = self.bot.join_voice_channel()
        except asyncio.TimeoutError as e:
            await ctx.send("Pas de vpn :s")
            return"""


def setup(bot):
    bot.add_cog(NetInfo(bot))

def teardown(bot):
    pass
