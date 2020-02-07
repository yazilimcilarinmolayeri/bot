# -*- coding: utf-8 -*-
#

import sys
import config
import traceback

from .utils import meta
from .utils import role
from .utils import emoji as e

import discord
from discord.utils import get
from discord.ext import commands
from discord.ext.commands import errors


class Events(commands.Cog):
    """The description for Events goes here."""

    def __init__(self, bot):
        self.bot = bot

    def get_emoji(self, emoji):
        if emoji.id == None:
            return e.unicode_to_name(emoji)
        else:
            return emoji.id

    def get_role(self, guild, emoji):
        return get(guild.roles, name=role.roles[str(emoji)])

    @commands.Cog.listener()
    async def on_command_error(self, ctx, err):
        # Çağrılan komutda eksik yada hatalı argüman var ise yardım mesajı gönderilir.
        if isinstance(err, errors.MissingRequiredArgument) or isinstance(
            err, errors.BadArgument
        ):
            helper = (
                str(ctx.invoked_subcommand)
                if ctx.invoked_subcommand
                else str(ctx.command)
            )
            await ctx.send_help(helper)

        elif isinstance(err, errors.CommandOnCooldown):
            await ctx.send(
                f"Bu komut bekleme modunda... {err.retry_after:.1f}s sonra tekrar dene!"
            )
        elif isinstance(err, commands.CommandInvokeError):
            original = err.original
            
            if not isinstance(original, discord.HTTPException):
                print(f'In {ctx.command.qualified_name}:', file=sys.stderr)
                traceback.print_tb(original.__traceback__)
                print(f'{original.__class__.__name__}: {original}', file=sys.stderr)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        await meta.update_activity_name(self.bot)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        await meta.update_activity_name(self.bot)

    # Bu kodlara el atılacak. Asıl fonksiyonlar utils altına alınacak.

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        guild_id = payload.guild_id
        channel_id = payload.channel_id
        message_id = payload.message_id
        user_id = payload.user_id
        emoji = payload.emoji

        if guild_id == config.ymy_guild_id:
            if (
                channel_id == config.reaction_role_channel_id
                and message_id in config.reaction_role_message_ids
            ):
                guild = self.bot.get_guild(id=guild_id)
                user = guild.get_member(user_id)

                try:
                    role = self.get_role(guild, self.get_emoji(emoji))
                    await user.add_roles(role)
                    await user.send(f"`{role}` rolü alındı.")

                except KeyError:
                    channel = self.bot.get_channel(channel_id)
                    message = await channel.fetch_message(message_id)
                    await message.remove_reaction(emoji=emoji, member=user)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        guild_id = payload.guild_id
        channel_id = payload.channel_id
        message_id = payload.message_id
        user_id = payload.user_id
        emoji = payload.emoji

        if guild_id == config.ymy_guild_id:
            if (
                channel_id == config.reaction_role_channel_id
                and message_id in config.reaction_role_message_ids
            ):
                guild = self.bot.get_guild(id=guild_id)
                user = guild.get_member(user_id)

                try:
                    role = self.get_role(guild, self.get_emoji(emoji))
                    await user.remove_roles(role)
                    await user.send(f"`{role}` rölü bırakıldı.")

                except KeyError:
                    pass


def setup(bot):
    bot.add_cog(Events(bot))
