# -*- coding: utf-8 -*-
#
# Copyright (C) 2019-2020, Yazılımcıların Mola Yeri (ymy-discord)
#

import config

import discord
from discord.ext import commands


"""
async def check_guild_permissions(ctx, perms, *, check=all):
    is_owner = await ctx.bot.is_owner(ctx.author)
    if is_owner:
        return True

    if ctx.guild is None:
        return False

    resolved = ctx.author.guild_permissions
    return check(getattr(resolved, name, None) == value for name, value in perms.items())
"""


def is_owner():
    def predicate(ctx):
        return ctx.message.author.id in config.owner_ids

    return commands.check(predicate)


def is_mod():
    def predicate(ctx):
        return ctx.message.author.id in config.mod_ids

    return commands.check(predicate)
