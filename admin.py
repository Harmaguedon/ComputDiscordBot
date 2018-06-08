import discord
from discord.ext import commands
import asyncio
import io
from utils import lower

class Admins:
    """Admins only commands"""

    bot = None

    def __init__(self, bot):
        self.bot = bot

    async def __local_check(self, ctx):
        return await self.bot.is_admin(ctx)

    @commands.command(name='addEmote', pass_context=True)
    async def command_addEmote(self, ctx, emote_name:lower):
        attachments = ctx.message.attachments
        guild = ctx.guild
        fp = io.BytesIO()

        if len(attachments) == 0:
            await ctx.send("Error : You have to attach a picture to the command")
            return
        elif len(attachments) > 1:
            await ctx.send("Error : You have to attach only one picture to the command")
            return
        attachment = attachments[0]

        try:
            await attachment.save(fp)
        except Exception as e:
            await ctx.send("Error : Failing to load the file {} please retry".format(attachment.filename))
            return

        try:
            await guild.create_custom_emoji(name=emote_name, image=fp.getvalue())
        except discord.HTTPException as e:
            await ctx.send("Faild to upload the picture")
            return
        except discord.Forbidden as e:
            await ctx.send("You havn't the right to add an emote to this server")
            return

        await ctx.send("Emote {} added to the server".format(emote_name))

    @commands.command(name='removeEmote', pass_context=True)
    async def command_removeEmote(self, ctx, emote_name:lower):
        emoji = discord.utils.get(ctx.guild.emojis, name=emote_name)
        if not emoji:
            await ctx.send("Emote {} does not exist".format(emote_name))
            return
        await emoji.delete()
        await ctx.send("Emote {} removed".format(emote_name))

def setup(bot):
    bot.add_cog(Admins(bot))

def teardown(bot):
    pass
