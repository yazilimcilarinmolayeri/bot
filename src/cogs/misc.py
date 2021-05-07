# -*- coding: utf-8 -*-
#

import json
from datetime import datetime

import config
from .utils import http

import discord
from discord.ext import commands


class Misc(commands.Cog):
    """The description for Misc goes here."""

    def __init__(self, bot):
        self.bot = bot

    @commands.guild_only()
    @commands.command(aliases=["anket"])
    async def poll(self, ctx, question, *answers):
        """
        Anket oluşturur. En fazla 10 seçenek verebilirsin.
        
        Örnek:
            ymy+poll "Mandalina sever misin ?"
            ymy+poll "En sevdiğin meyve ?" Elma Armut Mandalina ...
        """

        embed = discord.Embed(color=self.bot.embed_color)
        embed.timestamp = datetime.utcnow()
        embed.title = f"\N{WHITE QUESTION MARK ORNAMENT} {question}"
        embed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)

        if answers == ():
            msg = await ctx.send(embed=embed)
            await msg.add_reaction("\N{THUMBS UP SIGN}")
            await msg.add_reaction("\N{THUMBS DOWN SIGN}")
            await msg.add_reaction("\N{SHRUG}")

        elif len(answers) <= 10:
            inner = [f"{i}\u20e3 : {answers[i]}" for i in range(len(answers))]
            embed.description = "\n".join(inner)

            msg = await ctx.send(embed=embed)

            for i in range(len(answers)):
                await msg.add_reaction(f"{i}\u20e3")

        else:
            await ctx.send_help(ctx.command)

    @commands.command(aliases=["urlkısalt"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def tinyurl(self, ctx, url: str):
        """Verilen URL adresini TinyUrl kullanarak kısaltır."""

        params = {
            "url": url,
        }

        async with ctx.typing():
            r = await http.post(url="http://tinyurl.com/api-create.php", data=params)

        await ctx.send(f"\N{LINK SYMBOL} <{r}>")
        
    @commands.command(aliases=["letmeegooglethat"])
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def google(self, ctx, keywords: str):
        """Verilen keywordleri letmegooglethat'da aratır."""
        
        keywords.replace(" ", "+")
        keywords = "https://letmegooglethat.com/?q=" + keywords
        
        await ctx.send(f"{keywords}")    

    @commands.command(aliases=["ekrangörüntüsü"])
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def ss(self, ctx, url: str, full_page: bool = 0):
        """Verilen website adresinin ekran görüntüsünü üretir."""

        # Aylık limit, 100 farklı ekran görüntüsü.
        # https://screenshotapi.net/
        # fresh: bool = 0
        # user_agent: str = " "

        params = {
            "url": url,
            "token": config.screenshot_api["token"],
            "full_page": full_page,
            "accept_languages": "tr-TR",
        }

        info_message = await ctx.send("Bu işlem birazcık uzun sürebilir...")

        async with ctx.typing():
            r = await http.post(
                url="https://screenshotapi.net/api/v1/screenshot",
                data=params,
                res_method="json",
            )

        embed = discord.Embed(color=self.bot.embed_color, timestamp=datetime.utcnow())
        try:
            embed.description = "**" + r["url"] + "**"
            embed.set_image(url=r["screenshot"])
        except KeyError:
            await info_message.edit(content="Alan adı çözülemedi!")
            return
        embed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
        await info_message.edit(content="", embed=embed)


def setup(bot):
    bot.add_cog(Misc(bot))
