# -*- coding: utf-8 -*-
#
# Yardımcı fonksiyonlar...
#

from collections import Counter

import config

import discord


async def update_activity_name(bot):
    """Aktivite kısmına insan kullanıcı sayısını yazdırır."""

    guild = bot.get_guild(config.ymy_guild_id)
    # Bot miktarı True, bot olmayanların miktarı False anahtar isminde sayılır.
    # {"True": 0, "False": 0}
    human = Counter(str(m.bot) for m in guild.members)["False"]

    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching, name=f"{human:,d} üyeyi"
        )
    )
