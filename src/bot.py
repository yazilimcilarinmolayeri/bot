#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# Copyright (C) 2019-2020, Yazılımcıların Mola Yeri (ymy-discord)
#

import config

from cogs.utils import meta

import discord
from discord.ext import commands


description = """
YMY (Yazılımcıların Mola Yeri) geliştiricileri tarafından sunucu ihtiyaçları için yazılmış botum.
"""

extensions = [
    "events",
    "cogs.help",
    "cogs.admin",
    "cogs.mod",
    "cogs.info",
    "cogs.fun",
    "cogs.misc",
]


def get_prefix(bot, msg):
    user_id = bot.user.id
    return [f"<@!{user_id}> ", f"<@{user_id}> ", "ymy+", "+"]


class YMYBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=get_prefix, description=description, case_insensitive=True,
        )

        self.embed_color = 0x36393F

        for cog in extensions:
            try:
                self.load_extension(cog)
            except Exception as exc:
                print(f"{cog} {exc.__class__.__name__}: {exc}")

    @property
    def owner(self):
        return self.get_user(self.owner_id)

    def run(self):
        super().run(config.token, reconnect=True)


bot = YMYBot()


@bot.event
async def on_ready():
    print(f"{bot.user} (ID: {bot.user.id})")
    print(f"discord.py version: {discord.__version__}")

    await meta.update_activity_name(bot)


if __name__ == "__main__":
    bot.run()
