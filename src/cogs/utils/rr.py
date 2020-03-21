# -*- coding: utf-8 -*-
#
# YMYBot Copyright (C) 2019-2020 Yazılımcıların Mola Yeri (ymyoh)
# Reaksiyon Rol Sistemi
#

import json

import emoji as emo

import discord
from discord.utils import get


class ReactionRole:
    """Reaksiyon rol sınıfı."""

    def __init__(self, bot, payload):
        self.bot = bot
        self.payload = payload
        self.emoji = payload.emoji
        self.guild = self.bot.get_guild(id=payload.guild_id)
        self.member = self.guild.get_member(payload.user_id)
        self.get_data()

    def get_data(self):
        with open("src/cogs/utils/data/rr_data.json") as f:
            rr_data = json.load(f)

        self.rr_data = rr_data

    def unicode_to_shortcode(self, unicode_emoji):
        """Unicode olarak verilen emojinin adını döndürür."""

        return emo.demojize(unicode_emoji.name)

    def get_emoji(self, emoji):
        """Verilen emoji unicode ise adını, özel ise kimşiğini döndürür."""

        if emoji.is_unicode_emoji():
            return self.unicode_to_shortcode(emoji)
        else:
            pass

    def get_role(self, guild, emoji):
        """Reaksiyona eklelen emojiye karşılık gelen rolü döner."""

        return get(
            guild.roles,
            name=self.rr_data[str(self.payload.message_id)]["rr"][emoji[1:-1]],
        )

    def role_check(self):
        """Reaksiyona karşılık gelen rolün kullanıcıda olup olmadığına bakar."""

        self.role = self.get_role(self.guild, self.get_emoji(self.emoji))

        status = False
        for mr in self.member.roles:
            if mr.id == self.role.id:
                status = True
                break
            else:
                status = False

        return status

    async def remove_reaction(self):
        """Kullanıcının eklediği tepkiyi siler."""

        channel = self.bot.get_channel(self.payload.channel_id)
        message = await channel.fetch_message(self.payload.message_id)
        await message.remove_reaction(emoji=self.emoji, member=self.member)

    async def add_role(self):
        """Kullanıcıya rol ekler. Mesaj gönderir. Eklediği tepkiyi siler."""
        
        # Eğer rol sayısı 20'ye eşit yada fazla ise kullanıcı daha fazla rol alamaz.
        if len(self.member.roles) - 1 >= 20:
            await self.remove_reaction()
            await self.member.send(f"\N{NO ENTRY} En fazla 20 rol alabilirsin!")
            return

        await self.remove_reaction()
        await self.member.add_roles(self.role)
        await self.member.send(f"\N{INBOX TRAY} `{self.role.name}` rolü eklendi!")

    async def remove_role(self):
        """Kullanıcıdan rol siler. Mesaj gönderir. Eklediği tepkiyi siler."""

        await self.remove_reaction()
        await self.member.remove_roles(self.role)
        await self.member.send(f"\N{OUTBOX TRAY} `{self.role.name}` rolü silindi!")

    async def add_or_remove(self):
        """Eklenen tepkiye göre kullanıcının rolü yok ise ekler, var ise siler."""

        if self.member.bot:
            return

        if self.role_check():
            await self.remove_role()
        else:
            await self.add_role()
