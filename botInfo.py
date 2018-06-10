import discord
from discord.ext import commands
import asyncio
import inspect
from dbManager import preprocess_string
from datetime import datetime as dt
from utils import capitalize

class BotInfo:
    """Bot's information related commands"""

    bot = None

    def __init__(self, bot):
        self.bot = bot

    def format_help(self, ctx, em, cog=None):
        signatures_length = []
        commands = []
        for cmd in self.bot.commands:
            if not cmd.hidden:
                #__main__commands instances are None :p
                if cmd.instance is cog:
                    commands.append(cmd)
        if(len(commands) == 0):
            return
        sorted_commands = sorted(commands, key=lambda x: x.name)
        value = '{} : \n'.format('Admins only commands' if not cog else (self.bot.config["botInfo"]["missing doc message"] if not inspect.getdoc(cog) else inspect.getdoc(cog)))
        for c in sorted_commands:
            doc = c.short_doc if c.short_doc != "" else self.bot.config["botInfo"]["missing doc message"]
            value += '\t{}{} --> {}\n'.format(ctx.prefix, c.name, doc)
        name = 'Loading' if not cog else type(cog).__name__
        em.add_field(name=name, value=value, inline=False)
        return em

    @commands.command(name='help', pass_context=True)
    async def command_help(self, ctx, *args:capitalize):
        """Display help"""
        em = discord.Embed(title='Help :', color=0x1919A3)
        if len(args) == 0:
            args = list(self.bot.cogs.keys())
            args.append("Loading")
        args = sorted(args)
        for arg in args:
            cog = self.bot.get_cog(arg)
            if cog or arg == "Loading":
                self.format_help(ctx, em, cog)
        await ctx.send(embed=em)

    @commands.command(name='uptime', pass_context=True)
    async def command_uptime(self, ctx):
        """Display bot uptime"""
        time = dt.utcnow() - self.bot.launch_time
        mins, secs = divmod(int(time.total_seconds()), 60)
        hours, mins = divmod(mins, 60)
        days, hours = divmod(hours, 24)
        await ctx.send("Uptime : {}d {}h {}m {}s".format(days, hours, mins, secs))

    @commands.command(name='issueOpen', pass_context=True)
    async def command_issueOpen(self, ctx, *args):
        """Notify an issue"""
        request = 'INSERT INTO issues VALUES (DEFAULT, \'{}\');'.format(preprocess_string(' '.join(args)))
        response = await self.bot.db.execute(request)
        if response == 'INSERT 0 1':
            await ctx.send("Issue added")
        else:
            await ctx.send("Failure")

    @commands.command(name='issueClosed', pass_context=True)
    async def command_issueClosed(self, ctx, id):
        """Close an issue"""
        request = 'DELETE FROM issues WHERE id={};'.format(id)
        response = await self.bot.db.execute(request)
        if response == 'DELETE 1':
            await ctx.send('Issue {} closed'.format(id))
        else:
            await ctx.send('Issue {} does not exists'.format(id))

    @commands.command(name='issuesList', pass_context=True)
    async def command_issuesList(self, ctx):
        """List all the issues"""
        request = 'SELECT * FROM issues ORDER BY id;'
        issues = await self.bot.db.fetch(request)
        em = discord.Embed(title='Issues :', color=0x1919A3)
        for issue in issues:
            em.add_field(name=issue['id'], value=issue['description'], inline=False)
        await ctx.send(embed=em)

    @commands.command(name='ideaOpen', pass_context=True)
    async def command_ideaOpen(self, ctx, *args):
        """Propose an idea"""
        request = 'INSERT INTO ideas VALUES (DEFAULT, \'{}\');'.format(preprocess_string(' '.join(args)))
        response = await self.bot.db.execute(request)
        if response == 'INSERT 0 1':
            await ctx.send("Idea added")
        else:
            await ctx.send("Failure")

    @commands.command(name='ideaClose', pass_context=True)
    async def command_ideaClosed(self, ctx, id):
        """Close an idea"""
        request = 'DELETE FROM ideas WHERE id={};'.format(id)
        response = await self.bot.db.execute(request)
        if response == 'DELETE 1':
            await ctx.send('Idea {} closed'.format(id))
        else:
            await ctx.send('Idea {} does not exists'.format(id))

    @commands.command(name='ideasList', pass_context=True)
    async def command_ideasList(self, ctx):
        """List all the ideas"""
        request = 'SELECT * FROM ideas ORDER BY id;'
        ideas = await self.bot.db.fetch(request)
        em = discord.Embed(title='Ideas :', color=0x1919A3)
        for idea in ideas:
            em.add_field(name=idea['id'], value=idea['description'], inline=False)
        await ctx.send(embed=em)


def setup(bot):
    bot.add_cog(BotInfo(bot))

def teardown(bot):
    pass
