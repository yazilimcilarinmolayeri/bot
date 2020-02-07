# -*- coding: utf-8 -*-
#

from .utils import checks

import discord
from discord.ext import commands


class Mod(commands.Cog):
    """The description for Mod goes here."""

    def __init__(self, bot):
        self.bot = bot

    @commands.guild_only()
    @commands.command(aliases=["süpür"])
    @checks.has_permissions(manage_messages=True)
    async def clean(self, ctx, amount: int = 1):
        """Kanaldaki mesajları verilen miktar kadar temizler."""

        channel = ctx.message.channel

        messages = list()
        # Verdiğimiz komutda bir mesaj olduğu için fazladan 1 tane daha siliyoruz.
        async for message in channel.history(limit=int(amount) + 1):
            messages.append(message)

        await channel.delete_messages(messages)
        await channel.send(f"`{len(messages)-1}` mesaj süpürüldü!", delete_after=3)

    @commands.guild_only()
    @commands.command(aliases=["yazdır"])
    @checks.is_mod()
    async def echo(self, ctx, channel: discord.TextChannel, *, content: str):
        """Belirlenen kanala mesaj içeriğini gönderir."""

        await channel.send(content)


def setup(bot):
    bot.add_cog(Mod(bot))
