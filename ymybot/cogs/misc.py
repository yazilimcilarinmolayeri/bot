# -*- coding: utf-8 -*-
#
# Copyright (C) 2019, Yazılımcıların Mola Yeri (ymy-gitrepo)
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

import time

from cogs.utils import emoji

from discord.ext import commands
import discord


class Misc(commands.Cog):
    """The description for Misc goes here."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=[])
    async def ping(self, ctx):
        before = time.monotonic()
        message = await ctx.send("Pinging...")

        ping = (time.monotonic() - before) * 1000
        await message.edit(content=f"{emoji.pong} Pong! `{int(ping)}`ms")


def setup(bot):
    bot.add_cog(Misc(bot))
