# -*- coding: utf-8 -*-
#

import random
from datetime import datetime

import config
from .utils import http

import discord
from discord.ext import commands


class Fun(commands.Cog, name="Funny"):
    """The description for Fun goes here."""

    def __init__(self, bot):
        self.bot = bot
        self.loads_meme_commands()

    def loads_meme_commands(self):
        # teamplate: {"name": "", "lname": "", "id": }
        meme_cmds = [
            {"name": "stonks", "lname": "Stonks", "id": 186821996},
            {"name": "twobuttons", "lname": "Two Buttons", "id": 87743020},
            {"name": "buttonslam", "lname": "Blank Nut Button", "id": 119139145},
            {"name": "changemymind", "lname": "Change My Mind", "id": 129242436},
            {"name": "maurice", "lname": "Hide the Pain Harold", "id": 27813981},
            {"name": "batmanslap", "lname": "Batman Slapping Robin", "id": 438680},
            {"name": "winniepooh", "lname": "Tuxedo Winnie The Pooh", "id": 178591752},
            {"name": "womenyelling", "lname": "	Woman Yelling At Cat", "id": 188390779},
            {"name": "disappointed", "lname": "Disappointed Black Guy", "id": 50421420},
            {
                "name": "thinkingguy",
                "lname": "Roll Safe Think About It",
                "id": 89370399,
            },
        ]

        # {"name": "spiderman", "lname": "Spiderman Presentation", "id": 176754986}
        # {"name": "dogecloud", "lname": "Doge Cloud", "id": 221181003}
        # {"name": "monkeypuppet", "lname": "Monkey Puppet", "id": 14890980}

        for row in meme_cmds:
            command = commands.Command(
                name=row["name"],
                func=Fun.meme_command,
                help=f"`{row['lname'].strip()}` adlı meme'yi üretir.",
            )

            command.meme_id = row["id"]
            command.cog = self
            self.meme.add_command(command)

    # =============================================================================
    #     def get_dong(self, user):
    #         """Penis'in ascci içeriğini ve uzunluk değerini döndürür."""
    #
    #         # state = random.getstate()
    #         random.seed(user.id)
    #         size = "_" * random.randint(0, 30)
    #
    #         #
    #         # seed() fonksiyonu, rastgele sayılar üretirken kullanılan tam sayı
    #         # başlangıç değerini ayarlar. Eğer hep o sabit sayıyı verirsen hep
    #         # aynı randomu üretirler, çünkü aslında random değiller :)
    #         #
    #
    #         dong_ascii = f"  ###{size} _\n    _{size}│_-)\n(_)_)"
    #         # random.setstate(state)
    #
    #         return {"ascii": dong_ascii, "size": len(size)}
    #
    #     @commands.guild_only()
    #     @commands.group(aliases=["çük"], invoke_without_command=True, hidden=True)
    #     @commands.cooldown(1, 5, commands.BucketType.user)
    #     async def dong(self, ctx, *, user: discord.Member = None):
    #         """Kullanıcının penis boyunu hesaplar. Bu değer asla ama asla değişmez!"""
    #
    #         if user is None:
    #             user = ctx.author
    #
    #         dong = self.get_dong(user)
    #
    #         embed = discord.Embed(color=self.bot.embed_color)
    #         embed.title = f"{user} Dong Size"
    #         embed.description = f"```{dong['ascii']}```"
    #         await ctx.send(embed=embed)
    #
    #     @dong.command(aliases=["yarıştır"])
    #     async def race(self, ctx, *, user: discord.Member):
    #         """İki kullanıcının penis boyunu yarıştırır."""
    #
    #         author = ctx.author
    #
    #         a_dong = self.get_dong(author)
    #         u_dong = self.get_dong(user)
    #
    #         embed = discord.Embed(color=self.bot.embed_color)
    #         embed.title = f"{author} vs {user}"
    #         embed.description = f"```{a_dong['ascii']}\n\n{u_dong['ascii']}```"
    #         await ctx.send(embed=embed)
    # =============================================================================

    @commands.command(aliases=["kedi"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def cat(self, ctx):
        """Ratgele bir kedi resmi gönderir."""

        async with ctx.typing():
            r = await http.get(
                url="https://nekos.life/api/v2/img/meow", res_method="json"
            )

        await ctx.send(
            embed=discord.Embed(color=self.bot.embed_color).set_image(url=r["url"])
        )

    @commands.group(invoke_without_command=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def meme(self, ctx, command=None):
        """
        Verilen argümanlar dahilinde meme üretir.
        
        Örnek:
            ymy+meme winniepooh "deneme" "deneme"
        """

        cmds = [f"`{c.name}`" for c in self.bot.get_command(str(ctx.command)).commands]

        embed = discord.Embed(color=self.bot.embed_color)
        embed.title = "Meme Komutları"
        embed.description = ", ".join(cmds)
        embed.set_footer(text=f"{ctx.prefix}help meme <command>")

        await ctx.send(embed=embed)

    async def meme_generator(self, ctx, meme_id: int, text0, text1):
        """
        imgflip.com API'sini kullanarak meme üreten fonksiyon.
        Meme ID'leri: https://api.imgflip.com/popular_meme_ids
        """

        params = {
            "template_id": meme_id,
            "username": config.imgflip_api["username"],
            "password": config.imgflip_api["password"],
            "text0": text0,
            "text1": text1,
        }

        async with ctx.typing():
            r = await http.post(
                "https://api.imgflip.com/caption_image", data=params, res_method="json"
            )

        return r["data"]["url"]

    async def meme_command(self, ctx, text0, text1=""):
        embed = discord.Embed(color=self.bot.embed_color)
        embed.timestamp = datetime.utcnow()

        img_url = await self.meme_generator(ctx, ctx.command.meme_id, text0, text1)

        embed.set_image(url=img_url)
        embed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def tweet(self, ctx, *, text: str):
        """Sahte tweet görseli hazırlar."""

        username = ctx.author.name

        # params = {
        #     "type": "tweet",
        #     "username": username,
        #     "text": text,
        # }

        async with ctx.typing():
            r = await http.get(
                url="https://nekobot.xyz/api/imagegen?"
                f"type=tweet&username={username}&text={text}",
                res_method="json",
            )

            if r["status"] != 200:
                return await ctx.send("API bağlantısı başarısız...")

        embed = discord.Embed(color=self.bot.embed_color)
        embed.set_image(url=r["message"])
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def deepfry(self, ctx, user: discord.Member = None):
        """Kişinin profil görseline kızartma efekti ekler."""

        user = user or ctx.author
        avatar = user.avatar_url

        # params = {
        #     "type": "deepfry",
        #     "image": avatar,
        # }

        async with ctx.typing():
            r = await http.get(
                url="https://nekobot.xyz/api/imagegen?" f"type=deepfry&image={avatar}",
                res_method="json",
            )

            if r["status"] != 200:
                return await ctx.send("API bağlantısı başarısız...")

        embed = discord.Embed(color=self.bot.embed_color)
        embed.set_image(url=r["message"])
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Fun(bot))
