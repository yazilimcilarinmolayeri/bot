# -*- coding: utf-8 -*-
#
# Copyright (C) 2019-2020, Yazılımcıların Mola Yeri (ymy-discord)
#

import config

import discord


async def update_activity_name(bot):
    """Aktivite kısmına insan kullanıcı sayısını yazdırır."""

    guild = bot.get_guild(config.ymy_guild_id)

    b = 0
    for m in guild.members:
        if m.bot == True:
            b += 1

    members = len(guild.members) - b

    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching, name=f"{members:,d} üyeyi"
        )
    )
