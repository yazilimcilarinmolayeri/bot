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


def setup(bot):
    bot.add_cog(Misc(bot))
