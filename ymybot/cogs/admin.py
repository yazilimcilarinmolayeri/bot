# -*- coding: utf-8 -*-
#
# Copyright (C) 2019-2020, Yazılımcıların Mola Yeri (ymy-discord)
#

import copy
import asyncio
import subprocess

from cogs.utils import checks

# from cogs.utils import emoji

from discord.ext import commands
import discord


class Admin(commands.Cog):
    """The description for Admin goes here."""

    def __init__(self, bot):
        self.bot = bot

    async def run_process(self, command):
        try:
            process = await asyncio.create_subprocess_shell(
                command, stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
            result = await process.communicate()
        except NotImplementedError:
            process = subprocess.Popen(
                command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
            result = await self.bot.loop.run_in_executor(None, process.communicate)

        return [output.decode() for output in result]

    @checks.is_owner()
    @commands.command(aliases=["yükle"], hidden=True)
    async def load(self, ctx, *, module):
    	""" Modülü yükler """
        try:
            self.bot.load_extension(module)
        except commands.ExtensionError as e:
            await ctx.send(f"{e.__class__.__name__}: {e}")
        else:
            await ctx.send("Modül yüklendi!")

    @checks.is_owner()
    @commands.command(aliases=["kaldır"], hidden=True)
    async def unload(self, ctx, *, module):
    	""" Modülü pasif hale getirir"""
        try:
            self.bot.unload_extension(module)
        except commands.ExtensionError as e:
            await ctx.send(f"{e.__class__.__name__}: {e}")
        else:
            await ctx.send("Modül kaldırıldı!")

    @checks.is_owner()
    @commands.command(aliases=["yenile"], hidden=True)
    async def reload(self, ctx, *, module):
    	""" Modülü yeniden başlatır """
        try:
            self.bot.reload_extension(module)
        except commands.ExtensionError as e:
            await ctx.send(f"{e.__class__.__name__}: {e}")
        else:
            await ctx.send("Modül yenilendi!")

    @commands.command(aliases=["kapat"], hidden=True)
    async def off(self, ctx):
    	""" Botu kapatır """
        await ctx.send("Bot kapatılıyor...")
        await self.bot.logout()

    @checks.is_owner()
    @commands.command(aliases=["yap"], hidden=True)
    async def do(self, ctx, times: int, *, command):
    	""" Komutları belirlenen sayıda tekrarlar """
        msg = copy.copy(ctx.message)
        msg.content = ctx.prefix + command

        new_ctx = await self.bot.get_context(msg, cls=type(ctx))

        for i in range(times):
            await new_ctx.reinvoke()

    @checks.is_owner()
    @commands.command(aliases=["sh", "kabuk"], hidden=True)
    async def shell(self, ctx, *, command):
    	""" Kabuk komutlarını çalıştıtır """
        async with ctx.typing():
            stdout, stderr = await self.run_process(command)

        if stderr:
            text = f"stdout:\n{stdout}\nstderr:\n{stderr}"
        else:
            text = stdout

        await ctx.send(f"Çıktı:\n```{text}```")


def setup(bot):
    bot.add_cog(Admin(bot))
