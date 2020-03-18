# -*- coding: utf-8 -*-
#
# admin komutları yazılırken yararlanılan kaynaklar:
# - https://github.com/Rapptz/RoboDanny/blob/rewrite/cogs/admin.py
# - https://github.com/AlexFlipnote/discord_bot.py/blob/master/cogs/admin.py
#

import io
import copy
import asyncio
import textwrap
import traceback
import subprocess
from contextlib import redirect_stdout

import discord
from discord.ext import commands


class Admin(commands.Cog):
    """The description for Admin goes here."""

    def __init__(self, bot):
        self.bot = bot
        self._last_result = None

    async def cog_check(self, ctx):
        return await self.bot.is_owner(ctx.author)

    def cleanup_code(self, content):
        """Automatically removes code blocks from the code."""
        # remove ```py\n```
        if content.startswith("```") and content.endswith("```"):
            return "\n".join(content.split("\n")[1:-1])

        # remove `foo`
        return content.strip("` \n")

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

    @commands.command(aliases=["yükle"], hidden=True)
    async def load(self, ctx, *, module: str):
        """Modülü yükler."""

        try:
            self.bot.load_extension(module)
        except commands.ExtensionError as e:
            await ctx.send(f"{e.__class__.__name__}: {e}")
        else:
            await ctx.message.add_reaction("\u2705")

    @commands.command(aliases=["kaldır"], hidden=True)
    async def unload(self, ctx, *, module: str):
        """Modülü kaldırır."""

        try:
            self.bot.unload_extension(module)
        except commands.ExtensionError as e:
            await ctx.send(f"{e.__class__.__name__}: {e}")
        else:
            await ctx.message.add_reaction("\u2705")

    @commands.command(aliases=["yenile"], hidden=True)
    async def reload(self, ctx, *, module: str):
        """Modülü yeniden yükler."""
        try:
            self.bot.reload_extension(module)
        except commands.ExtensionError as e:
            await ctx.send(f"{e.__class__.__name__}: {e}")
        else:
            await ctx.message.add_reaction("\u2705")

    @commands.command(aliases=["kapat"], hidden=True)
    async def off(self, ctx):
        """Botu devre dışı bırakır."""

        await ctx.message.add_reaction("\u2705")
        await self.bot.logout()

    @commands.command(aliases=["yap"], hidden=True)
    async def do(self, ctx, times: int, *, command: str):
        """Bir komutu belirtilen sayıda tekrarlar."""

        msg = copy.copy(ctx.message)
        msg.content = ctx.prefix + command
        new_ctx = await self.bot.get_context(msg, cls=type(ctx))

        for i in range(times):
            await new_ctx.reinvoke()

    @commands.command(aliases=["sh", "kabuk"], hidden=True)
    async def shell(self, ctx, *, command: str):
        """Shell/kabuk komutlarını çalıştırır."""

        async with ctx.typing():
            stdout, stderr = await self.run_process(command)

        if stderr:
            output = f"stdout:\n{stdout}\nstderr:\n{stderr}"
        else:
            output = stdout

        await ctx.send(f"```sh\n{output}```")

    @commands.command(name="eval", hidden=True)
    async def _eval(self, ctx, *, body: str):
        """Python kodlarını yorumlar."""

        env = {
            "bot": self.bot,
            "ctx": ctx,
            "channel": ctx.channel,
            "author": ctx.author,
            "guild": ctx.guild,
            "message": ctx.message,
            "_": self._last_result,
        }

        env.update(globals())

        body = self.cleanup_code(body)
        stdout = io.StringIO()

        to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'

        try:
            exec(to_compile, env)
        except Exception as e:
            return await ctx.send(f"```py\n{e.__class__.__name__}: {e}\n```")

        func = env["func"]
        try:
            with redirect_stdout(stdout):
                ret = await func()
        except Exception as e:
            value = stdout.getvalue()
            await ctx.send(f"```py\n{value}{traceback.format_exc()}\n```")
        else:
            value = stdout.getvalue()
            try:
                await ctx.message.add_reaction("\u2705")
            except:
                pass

            if ret is None:
                if value:
                    await ctx.send(f"```py\n{value}\n```")
            else:
                self._last_result = ret
                await ctx.send(f"```py\n{value}{ret}\n```")


def setup(bot):
    bot.add_cog(Admin(bot))
