#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
#
# YMYBot Copyright (C) 2019-2020 Yazılımcıların Mola Yeri (ymyoh)
# Davet bağlantısı: https://discord.gg/KazHgb2
#

import ssl
import aiohttp
from collections import Counter

import config

import discord
from discord.ext import commands


description = """
YMY (Yazılımcıların Mola Yeri) geliştiricileri tarafından sunucu ihtiyaçları için yazılmış bot.
"""

extensions = [
    "cogs.events",
    "cogs.admin",
    "cogs.mod",
    "cogs.info",
    "cogs.fun",
    "cogs.misc",
    "cogs.help",
    "cogs.tureng",
]


def get_prefix(bot, msg):
    user_id = bot.user.id
    return [f"<@!{user_id}> ", f"<@{user_id}> "] + config.prefix


custom_context = ssl.create_default_context()
conn = aiohttp.TCPConnector(ssl=custom_context)


class YMYBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=get_prefix, description=description, case_insensitive=True,
        )

        self.uptime = ""
        self.embed_color = 0x36393F
        self.owner_ids = set(config.owner_ids)
        self.session = aiohttp.ClientSession(loop=self.loop, connector=conn)

        self._auto_spam_count = Counter()
        self.spam_control = commands.CooldownMapping.from_cooldown(
            10, 12.0, commands.BucketType.user
        )

        for cog in extensions:
            try:
                self.load_extension(cog)
            except Exception as exc:
                print(f"{cog} {exc.__class__.__name__}: {exc}")

        #
        # jishaku: A debugging and testing cog for discord.py rewrite bots.
        # Source code: https://github.com/Gorialis/jishaku
        #

        self.load_extension("jishaku")

    @property
    def owners(self):
        return [self.get_user(i) for i in self.owner_ids]

    @property
    def config(self):
        return __import__("config")

    async def on_resumed(self):
        print("Resumed...")

    async def close(self):
        await super().close()
        await self.session.close()

    def run(self):
        super().run(config.token, reconnect=True)


bot = YMYBot()
# __import__("generator").command_guide_builder(bot)


if __name__ == "__main__":
    bot.run()
