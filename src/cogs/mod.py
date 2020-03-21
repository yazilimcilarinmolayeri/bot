# -*- coding: utf-8 -*-
#

import json
import string
import emoji as emo

import config
from .utils import checks

import discord
from discord.ext import commands


class Mod(commands.Cog, name="Moderation"):
    """The description for Mod goes here."""

    def __init__(self, bot):
        self.bot = bot

    @commands.guild_only()
    @commands.command(aliases=["süpür"])
    @checks.has_permissions(manage_messages=True)
    async def clean(self, ctx, amount: int):
        """Kanaldaki mesajları verilen miktar kadar temizler."""

        channel = ctx.message.channel
        # Verdiğimiz komutda bir mesaj olduğu için fazladan 1 tane daha siliyoruz.
        deleted = await channel.purge(limit=amount + 1)

        await ctx.send(f"`{len(deleted)-1}` mesaj süpürüldü.", delete_after=3.0)

    @commands.guild_only()
    @commands.group(aliases=["yazdır"], invoke_without_command=True)
    @checks.is_mod()
    async def echo(self, ctx, channel: discord.TextChannel, *, content: str):
        """Belirlenen kanala mesaj içeriğini gönderir."""

        await channel.send(content)

    @echo.command()
    async def embed(self, ctx, channel: discord.TextChannel, *, content):
        """
        JSON veri formatında verilen içeriği embed olarak gönderir.
        İçerik üretmek için: https://bastion.traction.one/embedbuilder/
        """

        embed = discord.Embed.from_dict(json.loads(content))
        await channel.send(embed=embed)

    @echo.command()
    async def dm(self, ctx, user_id, *, content):
        """Kimliği verilen kullanıcıya verilen içeriği doğrudan gönderir."""
        
        user = await self.bot.fetch_user(user_id)
        await user.send(content)
        
        dmlog = self.bot.get_channel(687804890860486762)
        embed = discord.Embed(color=discord.Colour.green())
        embed.description = content
        embed.set_author(name=user, icon_url=user.avatar_url)
        embed.set_footer(text=f"ID: {user.id}")

        await dmlog.send(embed=embed)

    @commands.guild_only()
    @commands.command()
    @checks.is_mod()
    async def placerr(self, ctx):
        """
        Deneyseldir. data/rr_data.json dosyasındaki verileri kullanrak reaksiyon rol 
        mesajlarını günceller.
        """
        
        with open("src/cogs/utils/data/rr_data.json") as f:
            rr_data = json.load(f)
        
        channel = self.bot.get_channel(config.rr_channel_id)
        
        def get_unicode(name):
            return emo.emojize(f":{name}:")
        
        for message_id in rr_data.keys():
            rr = rr_data[message_id]["rr"]
            
            embed = discord.Embed(color=self.bot.embed_color)
            embed.title = rr_data[message_id]["title"]
            embed.description = "\n".join([f"{get_unicode(i)} : {rr[i]}" for i in rr])
            
            message = await channel.fetch_message(message_id)
            await message.edit(embed=embed)
            
            for i in rr.keys():
                await message.add_reaction(get_unicode(i))
        
        await ctx.message.add_reaction("\u2705")
    
        
def setup(bot):
    bot.add_cog(Mod(bot))
