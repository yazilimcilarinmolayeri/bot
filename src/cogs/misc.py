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
            ymy+poll "Mandalina sever misin ?" Evet Hayır
        """

        upvote = "<:upvote:675321144810930178>"
        downvote = "<:downvote:675321144727044123>"

        numbers = {
            0: "0️⃣",
            1: "1️⃣",
            2: "2️⃣",
            3: "3️⃣",
            4: "4️⃣",
            5: "5️⃣",
            6: "6️⃣",
            7: "7️⃣",
            8: "8️⃣",
            9: "9️⃣",
        }

        embed = discord.Embed(color=self.bot.embed_color)
        embed.title = question
        embed.timestamp = datetime.utcnow()
        embed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)

        if answers == ():
            msg = await ctx.send(embed=embed)
            await msg.add_reaction(upvote)
            await msg.add_reaction(downvote)

        elif len(answers) <= 10:
            inner = [f"{numbers[i]} : {answers[i]}" for i in range(len(answers))]
            embed.description = "\n".join(inner)

            msg = await ctx.send(embed=embed)

            for i in range(len(answers)):
                await msg.add_reaction(numbers[i])


def setup(bot):
    bot.add_cog(Misc(bot))
