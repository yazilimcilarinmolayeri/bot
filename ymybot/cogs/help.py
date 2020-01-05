# -*- coding: utf-8 -*-
#
# Copyright (C) 2019-2020, Yazılımcıların Mola Yeri (ymydepo)
#

from discord.ext import commands
import discord


class Help(commands.Cog):
    """The description for Help goes here."""

    def __init__(self, bot):
        self.bot = bot


def setup(bot):
    bot.add_cog(Help(bot))
