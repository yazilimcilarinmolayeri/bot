# -*- coding: utf-8 -*-
#

import time

import discord
from discord.ext import commands


class Misc(commands.Cog):
    """The description for Misc goes here."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["gecikme"])
    async def ping(self, ctx):
        """Botun gecikme süresini hesaplar."""

        before = time.monotonic()
        message = await ctx.send("Pinging...")
        # Ms cinsinden hesaplamak için 1000 ile çarpıyoruz.
        ping = (time.monotonic() - before) * 1000
        await message.edit(content=f"Pong! `{ping:.2f}`ms")


def setup(bot):
    bot.add_cog(Misc(bot))
