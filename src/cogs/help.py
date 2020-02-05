# -*- coding: utf-8 -*-
#
# Copyright (C) 2019-2020, Yazılımcıların Mola Yeri (ymy-discord)
#

import itertools

import discord
from discord.ext import commands


class HelpCommand(commands.HelpCommand):
    def __init__(self):
        super().__init__(
            command_attrs={
                "aliases": ["yardım"],
                "help": "Shows help about the bot, a command, or a category",
                "cooldown": commands.Cooldown(1, 3.0, commands.BucketType.member),
            }
        )

        self.owner_cogs = ["Admin"]
        self.ignore_cogs = ["Events", "Help"]

    def get_destination(self, no_pm: bool = False):
        if no_pm:
            return self.context.channel
        else:
            return self.context.author

    def get_command_signature(self, command):
        parent = command.full_parent_name
        if len(command.aliases) > 0:
            aliases = "|".join(command.aliases)
            fmt = f"[{command.name}|{aliases}]"
            if parent:
                fmt = f"{parent} {fmt}"
            alias = fmt
        else:
            alias = command.name if not parent else f"{parent} {command.name}"
        return f"{alias} {command.signature}"

    def common_command_formatting(self, embed, command):
        embed.title = self.get_command_signature(command)
        if command.description:
            embed.description = f"{command.description}\n\n{command.help}"
        else:
            embed.description = command.help or "Yardım bulunamadı..."

    async def send_bot_help(self, mapping):
        ctx = self.context
        owner = self.context.bot.owner

        embed = discord.Embed(color=ctx.bot.embed_color)
        
        embed.description = (
            f"Komutlar hakkında detaylı bilgi için: `[help|yardım] [command]`"
        )
        embed.set_author(name=ctx.bot.user.name)
        
        for extension in self.context.bot.cogs.values():
            if ctx.author == owner and extension.qualified_name in self.owner_cogs:
                continue
            if extension.qualified_name in self.ignore_cogs:
                continue

            commands = [f"**`{c.qualified_name}`**" for c in mapping[extension]]
            
            if len(commands) != 0:
                embed.add_field(
                    name=extension.qualified_name, value=", ".join(commands), inline=False)
            else:
                embed.add_field(
                    name=extension.qualified_name, value="\u200b", inline=False)
        
        await ctx.send(embed=embed)

    async def send_command_help(self, command):
        embed = discord.Embed(color=self.context.bot.embed_color)
        self.common_command_formatting(embed, command)
        await self.context.send(embed=embed)

    async def command_not_found(self, string):
        destination = self.get_destination(no_pm=True)
        await destination.send(f'"{string}" adlı bir komut bulunamadı.')


class Help(commands.Cog):
    """The description for Help goes here."""

    def __init__(self, bot):
        self._original_help_command = bot.help_command
        bot.help_command = HelpCommand()
        bot.help_command.cog = self
        self.bot = bot

    def cog_unload(self):
        self.bot.help_command = self._original_help_command


def setup(bot):
    bot.add_cog(Help(bot))
