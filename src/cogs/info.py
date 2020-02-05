# -*- coding: utf-8 -*-
#
# Copyright (C) 2019-2020, Yazılımcıların Mola Yeri (ymydepo)
#

import os
import inspect

import discord
from discord.ext import commands


class Info(commands.Cog):
    """The description for Info goes here."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["kaynak"])
    async def source(self, ctx, *, command: str = None):
        """ Tam kaynak kodunu veya komut kodlarını görüntüler. """

        source_url = "https://github.com/ymy-discord/ymybot"
        branch = "master"
        if command is None:
            return await ctx.send(source_url)

        if command == "help":
            src = type(self.bot.help_command)
            module = src.__module__
            filename = inspect.getsourcefile(src)
        else:
            obj = self.bot.get_command(command.replace(".", " "))
            if obj is None:
                return await ctx.send("Komut bulunamadı.")

            # since we found the command we're looking for, presumably anyway, let's
            # try to access the code itself
            src = obj.callback.__code__
            module = obj.callback.__module__
            filename = src.co_filename

        lines, firstlineno = inspect.getsourcelines(src)
        if not module.startswith("discord"):
            # not a built-in command
            location = os.path.relpath(filename).replace("\\", "/")
        else:
            location = module.replace(".", "/") + ".py"
            source_url = "https://github.com/Rapptz/discord.py"
            branch = "master"

        final_url = f"<{source_url}/blob/{branch}/{location}#L{firstlineno}-L{firstlineno + len(lines) - 1}>"
        await ctx.send(final_url)


def setup(bot):
    bot.add_cog(Info(bot))
