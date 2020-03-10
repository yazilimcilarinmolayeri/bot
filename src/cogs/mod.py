# -*- coding: utf-8 -*-
#

import json

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
    async def clean(self, ctx, amount: int):
        """Kanaldaki mesajları verilen miktar kadar temizler."""

        channel = ctx.message.channel
        # Verdiğimiz komutda bir mesaj olduğu için fazladan 1 tane daha siliyoruz.
        deleted = await channel.purge(limit=amount + 1)

        await ctx.send(f"`{len(deleted)-1}` mesaj süpürüldü.", delete_after=3.0)

    @commands.guild_only()
    @commands.group(aliases=["yazdır"], invoke_without_command=True)
    @checks.is_mod()
    async def echo(self, ctx, channel: discord.TextChannel, *, content: str):
        """Belirlenen kanala mesaj içeriğini gönderir."""

        await channel.send(content)

    @echo.command()
    async def embed(self, ctx, channel: discord.TextChannel, *, content):
        """
        JSON veri formatında verilen içeriği embed olarak gönderir.
        İçerik üretmek için: https://bastion.traction.one/embedbuilder/
        """

        embed = discord.Embed.from_dict(json.loads(content))
        await channel.send(embed=embed)


def setup(bot):
    bot.add_cog(Mod(bot))
