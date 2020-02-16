# -*- coding: utf-8 -*-
#

import random

import discord
from discord.ext import commands


class Fun(commands.Cog):
    """The description for Fun goes here."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["çük", "penis"], hidden=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def dong(self, ctx, *, user: discord.Member = None):
        """Kullanıcının penis uzunluğunu hesaplar. Bu değer asla ama asla değişmez!"""

        if user is None:
            user = ctx.author

        # state = random.getstate()
        random.seed(user.id)
        size = '_' * random.randint(0, 30)
        
        #
        # seed() fonksiyonu, rastgele sayılar üretirken kullanılan tam sayı 
        # başlangıç değerini ayarlar. Eğer hep o sabit sayıyı verirsen hep 
        # aynı randomu üretirler, çünkü aslında random değiller :)
        # 
        
        dong = f"  ###{size} _\n    _{size}│_-)\n(_)_)"
        # random.setstate(state)

        embed = discord.Embed(color=self.bot.embed_color)
        embed.title = f"{user} Dong Size"
        embed.description = f"```{dong}```"
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Fun(bot))
