# -*- coding: utf-8 -*-
#

import time
from datetime import datetime

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

    @commands.guild_only()
    @commands.command(aliases=["anket"])
    async def poll(self, ctx, question, *answers):
        """
        Anket oluşturur. En fazla 10 seçenek verebilirsin.
        
        Örnek:
            ymy+poll "Mandalina sever misin ?"
            ymy+poll "En sevdiğin meyve ?" Elma Armut Mandalina ...
        """

        upvote = "<:upvote:675321144810930178>"
        downvote = "<:downvote:675321144727044123>"

        emoji_letters = [
            "\N{REGIONAL INDICATOR SYMBOL LETTER A}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER B}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER C}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER D}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER E}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER F}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER G}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER H}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER I}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER J}",
        ]

        embed = discord.Embed(color=self.bot.embed_color)
        embed.title = question
        embed.timestamp = datetime.utcnow()
        embed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)

        if answers == ():
            msg = await ctx.send(embed=embed)
            await msg.add_reaction("\N{THUMBS UP SIGN}")
            await msg.add_reaction("\N{THUMBS DOWN SIGN}")
            await msg.add_reaction("\N{SHRUG}")

        elif len(answers) <= 10:
            inner = [f"{emoji_letters[i]} : {answers[i]}" for i in range(len(answers))]
            embed.description = "\n".join(inner)

            msg = await ctx.send(embed=embed)

            for i in range(len(answers)):
                await msg.add_reaction(emoji_letters[i])


def setup(bot):
    bot.add_cog(Misc(bot))
