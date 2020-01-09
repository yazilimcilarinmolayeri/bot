#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (C) 2019-2020, Yazılımcıların Mola Yeri (ymydepo)
#

import config

from discord.ext import commands
import discord


description = """
İhtiyaçlar dahilinde hazırlanmış çok amaçlı Discord botu.
"""


class YMYBot(commands.Bot):
    def __init__(self, **kwargs):
        super().__init__(
            command_prefix=commands.when_mentioned_or(config.prefix),
            description=description,
            **kwargs,
        )
        for cog in config.cogs:
            try:
                self.load_extension(cog)
            except Exception as exc:
                print(
                    f"Could not load extension {cog} due to {exc.__class__.__name__}: {exc}"
                )

    async def on_ready(self):
        print(f"Logged on as {self.user} (ID: {self.user.id})")
        print(f"discord.py version: {discord.__version__}")

    async def on_command_error(self, ctx, error):
        channel = ctx.message.channel

        error_embed = discord.Embed(color=0x36393F)
        error_embed.add_field(
            name="Komut yürütülürken hata oluştu !", value=f"`{error}`", inline=True
        )

        await channel.send(embed=error_embed)


def main():
    bot = YMYBot()
    bot.remove_command("help")
    bot.run(config.token)


if __name__ == "__main__":
    main()
