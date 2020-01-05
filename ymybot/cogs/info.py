# -*- coding: utf-8 -*-
#
# Copyright (C) 2019-2020, Yazılımcıların Mola Yeri (ymydepo)
#

from discord.ext import commands
import discord


class Info(commands.Cog):
    """The description for Info goes here."""

    def __init__(self, bot):
        self.bot = bot


def setup(bot):
    bot.add_cog(Info(bot))
