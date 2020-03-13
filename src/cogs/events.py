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
                print(f"In {ctx.command.qualified_name}:", file=sys.stderr)
                traceback.print_tb(original.__traceback__)
                print(f"{original.__class__.__name__}: {original}", file=sys.stderr)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        await meta.update_activity_name(self.bot)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        await meta.update_activity_name(self.bot)

    @commands.Cog.listener()
    async def on_message(self, message):
        author = message.author

        if message.author is self.bot.user:
            return

        if message.guild is None:
            dmlog = self.bot.get_channel(687804890860486762)
            embed = discord.Embed(color=self.bot.embed_color)
            embed.description = message.content
            embed.set_author(name=author, icon_url=author.avatar_url)
            embed.set_footer(text=f"ID: {message.author.id}")

            if message.attachments:
                attachment_url = message.attachments[0].url
                embed.set_image(url=attachment_url)

            await dmlog.send(embed=embed)

        if self.bot.user.mentioned_in(message) and message.mention_everyone is False:
            mentionlog = self.bot.get_channel(687805076857028671)
            embed = discord.Embed(color=self.bot.embed_color)
            embed.description = message.content
            embed.set_author(name=author, icon_url=author.avatar_url)
            embed.set_footer(text=f"ID: {message.author.id}")

            embed.add_field(
                name="Bahsetme Bilgisi",
                value=f"Sunucu: {author.guild}\n"
                f"ID: `{author.guild.id}`\n"
                f"Kanal: #{message.channel.name}\n"
                f"ID: `{message.channel.id}`",
            )

            if message.attachments:
                attachment_url = message.attachments[0].url
                embed.set_image(url=attachment_url)

            return await mentionlog.send(embed=embed)

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
                    await user.send(f"`{role}` rolü bırakıldı.")

                except KeyError:
                    pass


def setup(bot):
    bot.add_cog(Events(bot))
