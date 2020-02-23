# -*- coding: utf-8 -*-
#
# source/kaynak komutu kaynağı:
# - https://github.com/Rapptz/RoboDanny/blob/rewrite/cogs/meta.py#L328-L366
#

import os
import inspect

import discord
from discord.ext import commands


class Info(commands.Cog):
    """The description for Info goes here."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["kaynak"])
    async def source(self, ctx, *, command: str = None):
        """Botun GitHub'da bulunan kaynak kodlarını görüntüler."""

        source_url = "https://github.com/ymy-discord/ymybot"
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


def setup(bot):
    bot.add_cog(Info(bot))
