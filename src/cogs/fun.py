# -*- coding: utf-8 -*-
#

import random
from io import BytesIO
from datetime import datetime
from PIL import Image, ImageFilter

import config
from .utils import http

import discord
from discord.ext import commands


class Fun(commands.Cog, name="Funny"):
    """The description for Fun goes here."""

    def __init__(self, bot):
        self.bot = bot
        self.loads_meme_commands()

    async def get_image_bytes(self, image):
        async with self.bot.session.get(str(image)) as response:
            return await response.read()

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

    def loads_meme_commands(self):
        # teamplate: {"name": "", "lname": "", "id": }
        meme_cmds = [
            {"name": "stonks", "lname": "Stonks", "id": 186821996},
            {"name": "twobuttons", "lname": "Two Buttons", "id": 87743020},
            {"name": "thinkingguy", "lname": "Thinking Guy", "id": 89370399},
            {"name": "buttonslap", "lname": "Blank Nut Button", "id": 119139145},
            {"name": "changemymind", "lname": "Change My Mind", "id": 129242436},
            {"name": "maurice", "lname": "Hide the Pain Harold", "id": 27813981},
            {"name": "batmanslap", "lname": "Batman Slapping Robin", "id": 438680},
            {"name": "winniepooh", "lname": "Tuxedo Winnie The Pooh", "id": 178591752},
            {"name": "womenyelling", "lname": "	Woman Yelling At Cat", "id": 188390779},
            {"name": "disappointed", "lname": "Disappointed Black Guy", "id": 50421420},
        ]

        for row in meme_cmds:
            command = commands.Command(
                name=row["name"],
                func=Fun.meme_command,
                help=f"`{row['lname'].strip()}` adlı meme'yi üretir.",
            )

            command.meme_id = row["id"]
            command.cog = self
            self.meme.add_command(command)

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

    @commands.command(name="ayça_22", aliases=["ayca_22"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def ayca22(self, ctx, user: discord.Member = None):
        """Ayça_22 oturum açtı bildirimine kişinin avatarını ekler."""

        user = user or ctx.author
        avatar = user.avatar_url_as(static_format="png")

        avatar_bytes = await self.get_image_bytes(avatar)

        async with ctx.typing():
            with Image.open(BytesIO(avatar_bytes)) as img:
                ayca_22 = Image.open("src/cogs/utils/data/ayca_22.png")
                bg = Image.new("RGB", ayca_22.size, "white")
                img_small = img.resize((64, 64), Image.BILINEAR)

                bg.paste(img_small.resize((195, 195), Image.NEAREST), (5, 125))
                bg.paste(ayca_22, (0, 0), ayca_22.convert("RGBA"))

                output_buffer = BytesIO()
                bg.save(output_buffer, "png")
                output_buffer.seek(0)

        file = discord.File(fp=output_buffer, filename="image.png")
        embed = discord.Embed(color=self.bot.embed_color)
        embed.set_image(url="attachment://image.png")

        await ctx.send(file=file, embed=embed)


def setup(bot):
    bot.add_cog(Fun(bot))
