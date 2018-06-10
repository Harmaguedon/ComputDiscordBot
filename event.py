import discord
from discord.ext import commands
from datetime import datetime
import os
import io
import asyncio
import asyncpg
from dbManager import preprocess_string
from utils import lower

class Event:
    """Event organisation commands"""
    bot = None

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='event', pass_context=True)
    async def command_event(self, ctx, event_name:lower):
        """Display infos about an event : Usage !event event_name """
        request = 'SELECT * FROM events WHERE name=\'{}\';'.format(preprocess_string(event_name))
        row = await self.bot.db.fetchrow(request)
        if not row:
            await ctx.send('The event {} does not exists :s'.format(event_name))
        else:
            await ctx.send(row['description'])

    @commands.command(name='eventParticipants', pass_context=True)
    async def command_eventParticipants(self, ctx, event_name:lower):
        """List all the participants to an event : Usage !eventParticipants event_name """
        request = 'SELECT * FROM events_members WHERE name_event=\'{}\';'.format(preprocess_string(event_name))
        members = await self.bot.db.fetch(request)
        if not members:
            await ctx.send('The event {} does not exists :s'.format(event_name))
            return
        message = "Participants are : \n"
        for member in members:
            message += '\t{}'.format(member['name_member'])
        await ctx.send(message)

    @commands.command(name='eventCreate', pass_context=True)
    async def command_eventCreate(self, ctx, event_name:lower, event_description):
        """Create an event : Usage !eventCreate event_name event_description"""
        request = 'INSERT INTO events VALUES (\'{}\', \'{}\');'.format(preprocess_string(event_name), preprocess_string(event_description))
        try:
            await self.bot.db.execute(request)
            await ctx.send('Event {} created'.format(event_name))
        except asyncpg.exceptions.UniqueViolationError:
            await ctx.send('{} aleready exists'.format(event_name))

    @commands.command(name='eventDelete', pass_context=True)
    async def command_eventDelete(self, ctx, event_name:lower):
        """Delete an event : Usage !eventDelete event_name """
        request = 'DELETE FROM events WHERE name=\'{}\';'.format(preprocess_string(event_name))
        response = await self.bot.db.execute(request)
        if response != 'DELETE 1':
            await ctx.send('Event {} does not exists'.format(event_name))
        else:
            await ctx.send('Event {} removed'.format(event_name))

    @commands.command(name='eventJoin', pass_context=True)
    async def command_eventJoin(self, ctx, event_name:lower, member_name=None):
        """Join an event : Usage !eventJoin event_name """
        if not member_name:
            member_name = ctx.author.name
        request = 'INSERT INTO events_members VALUES (\'{}\', \'{}\')'.format(preprocess_string(event_name), preprocess_string(member_name))
        try:
            response = await self.bot.db.execute(request)
            await ctx.send('{} joined the event {}'.format(member_name, event_name))
        except asyncpg.exceptions.ForeignKeyViolationError:
            await ctx.send('{} is not an event'.format(event_name))
        except asyncpg.exceptions.UniqueViolationError:
            await ctx.send('{} is already in event {}'.format(member_name, event_name))


    @commands.command(name='eventLeave', pass_context=True)
    async def command_eventLeave(self, ctx, event_name:lower, member_name=None):
        """Leave an event : Usage !eventLeave event_name """
        if not member_name:
            member_name = ctx.author.name
        request = 'DELETE FROM events_members WHERE name_event=\'{}\' AND name_member=\'{}\''.format(preprocess_string(event_name), preprocess_string(member_name))
        response = await self.bot.db.execute(request)
        print(response)
        if response != 'DELETE 1':
            await ctx.send('{} is not in event {}'.format(member_name, event_name))
        else:
            await ctx.send('{} leaved the event {}'.format(member_name, event_name))

    @commands.command(name='eventList', pass_context=True)
    async def command_eventList(self, ctx):
        """List all the events : Usage !eventList"""
        request = 'SELECT * FROM events;'
        events = await self.bot.db.fetch(request)
        em = discord.Embed(title='Events :', color=0x1919A3)
        for event in events:
            em.add_field(name=event['name'], value=event['description'], inline=False)
        await ctx.send(embed=em)

def setup(bot):
    bot.add_cog(Event(bot))

def teardown(bot):
    pass
