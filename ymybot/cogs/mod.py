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

from discord.ext import commands
import discord


class Mod(commands.Cog):
    """The description for Mod goes here."""

    def __init__(self, bot):
        self.bot = bot


def setup(bot):
    bot.add_cog(Mod(bot))
