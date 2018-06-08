import discord
from discord.ext import commands
from datetime import datetime
import os
import io
import asyncio
from utils import lower, find_matching_files

class File:
    """Files managment commands"""
    bot = None
    path = None
    file_max_size = None

    def __init__(self, bot):
        self.bot = bot
        self.path = self.bot.config["file"]["folder path"]
        self.file_max_size = self.bot.config["file"]["file max size"] #8MB is the maximal size of a discord attachment
        self.folder_max_size = self.bot.config["file"]["folder max size"] #1GB

    @commands.command(name='fileRegister', pass_context=True)
    async def command_fileRegister(self, ctx, *args:lower):
        """Save the attached file : Usage !fileRegister [file_name]"""
        message = ""
        file_name = self.path
        clear_file_name = ""
        attachments = ctx.message.attachments
        if len(attachments) == 0:
            await ctx.send("Error : You have to attach a file to the command")
            return
        elif len(attachments) > 1:
            await ctx.send("Error : Files can only be registerd one at a time")
            return
        attachment = attachments[0]
        if attachment.size > self.file_max_size:
            await ctx.send("Error : The maximal file size is {:.2f}MB".format(self.file_max_size/(1024*1024)))
            return
        folder_size = sum(os.path.getsize(f) for f in os.listdir(self.path) if os.path.isfile(f))
        if folder_size + attachment.size > self.folder_max_size:
            await ctx.send("Error : Not enough free space available, {:.2f}MB neededs".format((attachment.size - (self.folder_max_size - folder_size))/(1024*1024)))
            return

        if len(args) == 0:
            file_name += attachment.filename
            clear_file_name += attachment.filename
        else:
            file_name += " ".join(args)
            clear_file_name += " ".join(args)

        if os.path.isfile(file_name):
            i = 1
            while os.path.isfile(file_name+"({})".format(i)):
                i += 1
            file_name += "({})".format(i)

        fp = io.BytesIO()
        try:
            await attachment.save(fp)
        except Exception as e:
            await ctx.send("Error : Failing to load the file {} please retry".format(clear_file_name))
            return
        with open(file_name, 'w+b') as f:
            f.write(fp.getvalue())
        await ctx.send("The file {} has been registered".format(clear_file_name))

    @commands.command(name='fileRemove', pass_context=True)
    async def command_remove(self, ctx, *args:lower):
        """Remove the specified files : Usage !fileList file_name_regex"""
        if len(args) == 0:
            await ctx.send("Error : You have to specify a file to remove")
            return
        matching_files = find_matching_files(self.path, *args)
        if len(matching_files) == 0:
            await ctx.send("Error : No matching file found")
            return
        for f in matching_files:
            os.remove(self.path+f)
            await ctx.send("The file {} has been removed".format(f))

    @commands.command(name='fileList', pass_context=True)
    async def command_register(self, ctx, *args:lower):
        """List all available files : Usage !fileList [file_name_regex]"""
        message = "List : \n"
        matching_files = find_matching_files(self.path, *args)
        for f in matching_files:
            message += '    {:7.3f}MB {}\n'.format(os.path.getsize(self.path+f)/(1024*1024), f)
        await ctx.send(message)

    @commands.command(name='fileRename', pass_context=True)
    async def command_rename(self, ctx, *args:lower):
        """Rename a file : Usage !fileRename old_regex new"""
        if len(args) < 2:
            await ctx.send("Error : You have to specify the old and new name")
            return
        if os.path.isfile(args[-1]):
            await ctx.send("Error : File {} already exists".format(args[-1]))
            return
        matching_files = find_matching_files(self.path, *args[:-1])
        if len(matching_files) == 0:
            await ctx.send("Error : No matching files founds")
            return
        elif len(matching_files) > 1:
            await ctx.send("Error : Ambiguous file name")
            return
        os.rename(self.path+matching_files[0], self.path+args[-1])
        await ctx.send("Name {} changed to {}".format(matching_files[0], args[-1]))


    @commands.command(name='file', pass_context=True)
    async def command_file(self, ctx, *args:lower):
        """Display a file : Usage !file file_name_regex"""
        if len(args) == 0:
            await ctx.send("You have to specify a file")
            return
        matching_files = find_matching_files(self.path, *args)
        if len(matching_files) == 0:
            await ctx.send("Error : No matching files founds")
            return
        for matching_file in matching_files:
            file_ = None
            with io.open(self.path+matching_file,"rb") as f:
                fb = io.BytesIO(f.read())
                file_ = discord.File(fb, matching_file)
            await ctx.send(file=file_)


def setup(bot):
    bot.add_cog(File(bot))

def teardown(bot):
    pass
