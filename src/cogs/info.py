# -*- coding: utf-8 -*-
#
# source/kaynak komutu kaynağı:
# - https://github.com/Rapptz/RoboDanny/blob/rewrite/cogs/meta.py#L328-L366
#

import os
import time
import psutil
import aiohttp
import inspect
import platform

import discord
from discord.ext import commands


class Info(commands.Cog, name="Information"):
    """The description for Info goes here."""

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

    @commands.command(aliases=["kaynak"])
    async def source(self, ctx, *, command: str = None):
        """Botun GitHub'da bulunan kaynak kodlarını görüntüler."""

        source_url = "https://github.com/ymyoh/ymybot"
        branch = "master"
        if command is None:
            return await ctx.send(source_url)
        if command == "help":
            src = type(self.bot.help_command)
            module = src.__module__
            filename = inspect.getsourcefile(src)
        else:
            obj = self.bot.get_command(command.replace(".", " "))
            if obj is None:
                return await ctx.send("Komut bulunamadı.")

            # since we found the command we're looking for, presumably anyway, let's
            # try to access the code itself
            src = obj.callback.__code__
            module = obj.callback.__module__
            filename = src.co_filename

        lines, firstlineno = inspect.getsourcelines(src)
        if not module.startswith("discord"):
            # not a built-in command
            location = os.path.relpath(filename).replace("\\", "/")
        else:
            location = module.replace(".", "/") + ".py"
            source_url = "https://github.com/Rapptz/discord.py"
            branch = "master"

        final_url = f"<{source_url}/blob/{branch}/{location}#L{firstlineno}-L{firstlineno + len(lines) - 1}>"
        await ctx.send(final_url)

    @commands.command()
    async def avatar(self, ctx, *, user: discord.Member = None):
        """Kullanıcının büyük boyutda avatarını gösterir."""

        user = user or ctx.author

        embed = discord.Embed(color=self.bot.embed_color)
        avatar = user.avatar_url_as(static_format="png")
        embed.set_author(name=user)
        embed.set_image(url=avatar)

        await ctx.send(embed=embed)

    @commands.command(aliases=["sys", "sistem"])
    async def system(self, ctx):
        """Botun çalıştığı sistem hakkında bilgi verir."""

        embed = discord.Embed(colour=self.bot.embed_color)
        embed.set_author(name=f"{self.bot.user.name} Sistem Bilgisi")

        embed.description = (
            "```HTTP\n"
            f"OS : {platform.platform()}\n"
            f"CPU: %{psutil.cpu_percent(interval=0.1)} "
            f"(Çekirdek: {psutil.cpu_count()}, Frekans: "
            f"{round(psutil.cpu_freq().current,2)} Mhz)\n"
            f"RAM: {round(psutil.virtual_memory().used/1048576)}/"
            f"{round(psutil.virtual_memory().total/1048576)} MB "
            f"(Boşta: {round(psutil.virtual_memory().available/1048576)}MB)\n"
            f"ROM: {round(psutil.disk_usage('/').used/1073741824,2)}/"
            f"{round(psutil.disk_usage('/').total/1073741824,2)} GB "
            f"(Boşta: {round(psutil.disk_usage('/').free/1073741824,2)}GB)"
            "```"
        )

        return await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Info(bot))
