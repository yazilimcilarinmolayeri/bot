# -*- coding: utf-8 -*-
#
# source/kaynak komutu kaynağı:
# - https://github.com/Rapptz/RoboDanny/blob/rewrite/cogs/meta.py#L328-L366
#

import os
import time
import json
import inspect
import humanize
from io import BytesIO
from bs4 import BeautifulSoup
from PIL import Image, ImageDraw

from .utils import http
from .utils import meta
from .utils.cv import Covid19

import discord
from discord.utils import get
from discord.ext import commands


class Info(commands.Cog, name="Information"):
    """The description for Info goes here."""

    def __init__(self, bot):
        self.bot = bot
        self.covid19 = Covid19(bot)

    async def get_image_bytes(self, image):
        async with self.bot.session.get(str(image)) as response:
            return await response.read()

    @commands.command(aliases=["gecikme"])
    async def ping(self, ctx):
        """Botun gecikme süresini hesaplar."""

        before = time.monotonic()
        message = await ctx.send("Pinging...")
        # Ms cinsinden hesaplamak için 1000 ile çarpıyoruz.
        ping = (time.monotonic() - before) * 1000
        await message.edit(content=f"Pong! `{ping:.2f}`ms")

    def get_bot_uptime(self):
        humanize.i18n.activate("tr_TR")
        return humanize.naturaldelta(self.bot.uptime)

    @commands.command()
    async def uptime(self, ctx):
        """Botun ne kadar süredir aktif olduğunu söyler."""

        await ctx.send(
            "\N{HOURGLASS WITH FLOWING SAND}" f"Uptime: **`{self.get_bot_uptime()}`**"
        )

    @commands.command(aliases=["kaynak"])
    async def source(self, ctx, *, command: str = None):
        """Botun GitHub'da bulunan kaynak kodlarını görüntüler."""

        source_url = "https://github.com/ymyoh/ymybot"
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

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.group(aliases=["cv", "covid19"], invoke_without_command=True)
    async def corona(self, ctx, country=None):
        """Virüsünün global istatistiklerini görüntüler."""

        async with ctx.typing():
            global_stats = await self.covid19.get_global_stats()
            countries = await self.covid19.get_countries()
            last_update = await self.covid19.last_update()

        if country != None:
            command = self.bot.get_command("cv country")
            await command.__call__(ctx=ctx, country=country)
            return

        confirmed = global_stats["confirmed"]
        recovered = global_stats["recovered"]
        deaths = global_stats["deaths"]

        mortality_rate = round((deaths / confirmed * 100), 2)
        recovery_rate = round((recovered / confirmed * 100), 2)

        embed = discord.Embed(color=self.bot.embed_color)
        embed.set_thumbnail(url=Covid19.corona_image)
        embed.title = "Global COVID-19 Virüsü İstatistikleri"

        embed.add_field(name="Doğrulanan Vaka", value=f"{Covid19.gold} {confirmed:,d}")
        embed.add_field(name="İyileşen Kişi", value=f"{Covid19.green} {recovered:,d}")
        embed.add_field(name="Ölen Kişi", value=f"{Covid19.red} {deaths:,d}")
        embed.add_field(name="Görülen Ülke", value=f"{len(countries):,d}")
        embed.add_field(name="İyileşme Oranı", value=f"{recovery_rate}%")
        embed.add_field(name="Ölüm Oranı", value=f"{mortality_rate}%")

        chart = meta.draw_horizontal_chart(confirmed, recovered, deaths)
        file = discord.File(fp=chart, filename="chart.png")
        embed.set_image(url="attachment://chart.png")

        embed.set_footer(
            text=f"Son güncelleme: {last_update}", icon_url=Covid19.reload_icon
        )
        await ctx.send(file=file, embed=embed)

    @corona.command(name="countries", aliases=["ülkeler"])
    async def corona_countries(self, ctx):
        """Virüs bulunan ülkelerin bir listesini döndürür."""

        country_name_list = {1: "", 2: "", 3: ""}
        page = 1

        async with ctx.typing():
            countries = await self.covid19.get_countries()

            for country in countries:
                country_name_list[page] += f"`{country[0]}`, "

                if len(country_name_list[page]) >= 800:
                    page += 1
                else:
                    pass

        embed = discord.Embed(color=self.bot.embed_color)
        embed.description = (
            f"Ülke istatistikleri için: `[corona|cv|covid19] [country_name]`"
        )
        embed.title = f"COVID-19 Virüsü Bulunan Ülkeler ({len(countries)})"

        for name in country_name_list:
            embed.add_field(
                name=f"Sayfa {name}", value=country_name_list[name][0:-2], inline=False
            )

        await ctx.send(embed=embed)

    @corona.command(name="country", aliases=["ülke"])
    async def corona_country(self, ctx, country):
        """Verilen ülkenin virüs istatistiklerini görüntüler."""

        async with ctx.typing():
            check = await self.covid19.country_name_check(country)

            if not check[0] == True:
                return await ctx.send("Geçersiz ülke kodu veya adı!")

            country_stats = await self.covid19.get_country_stats(country.lower())
            flag = await self.covid19.get_flag(check[1][1])

        confirmed = country_stats["confirmed"]
        recovered = country_stats["recovered"]
        deaths = country_stats["deaths"]
        mortality_rate = round((deaths / confirmed * 100), 2)
        recovery_rate = round((recovered / confirmed * 100), 2)

        embed = discord.Embed(color=self.bot.embed_color)
        embed.set_thumbnail(url=Covid19.corona_image)
        embed.title = f"COVID-19 Virüsü İstatistikleri"
        embed.description = f"{flag} {check[1][0]}"

        embed.add_field(name="Doğrulanan Vaka", value=f"{Covid19.gold} {confirmed:,d}")
        embed.add_field(name="İyileşen Kişi", value=f"{Covid19.green} {recovered:,d}")
        embed.add_field(name="Ölen Kişi", value=f"{Covid19.red} {deaths:,d}")
        embed.add_field(name="\u200b", value="\u200b")
        embed.add_field(name="İyileşme Oranı", value=f"{recovery_rate}%")
        embed.add_field(name="Ölüm Oranı", value=f"{mortality_rate}%")

        chart = meta.draw_horizontal_chart(confirmed, recovered, deaths)
        file = discord.File(fp=chart, filename="chart.png")
        embed.set_image(url="attachment://chart.png")

        embed.set_footer(
            text=f"Son güncelleme: {country_stats['lastUpdate']}",
            icon_url=Covid19.reload_icon,
        )
        await ctx.send(file=file, embed=embed)

    @corona.command(name="top", aliases=["üst"])
    async def corona_top(self, ctx):
        """Virüsden en çok etkilenen ülkeleri listeler."""

        async with ctx.typing():
            top_list = await self.covid19.get_top()

        embed = discord.Embed(color=self.bot.embed_color)
        embed.set_thumbnail(url=Covid19.corona_image)
        embed.title = f"En Çok COVID-19 Virüslü Vaka Bulunan {(len(top_list))} Ülke"

        for country in top_list:
            country_region = country.country_region
            flag = country.flag
            confirmed = country.confirmed
            recovered = country.recovered
            deaths = country.deaths

            value = f"Vaka: {confirmed:,d}\nÖlen: {recovered:,d}\nİyileşen: {deaths:,d}"
            embed.add_field(name=f"{flag} {country_region}", value=value)

        await ctx.send(embed=embed)

    @corona.command(name="image", aliases=["görsel"])
    async def corona_image(self, ctx):
        """Dünya geneli virüs istatistiklerini görsel olarak paylaşır."""

        embed = discord.Embed(color=self.bot.embed_color)
        embed.title = f"Global COVID-19 Virüsü İstatistik Grafiği"
        embed.set_image(url=Covid19.image)

        await ctx.send(embed=embed)

    @corona.command(name="info", aliases=["bilgi"])
    async def corona_info(self, ctx):
        """Virüsü hakkında detaylı bilgi verir."""

        with open("src/cogs/utils/data/covid19_info_data.json") as f:
            i = json.load(f)

        embed = discord.Embed(color=self.bot.embed_color)
        embed.title = "COVID-19 (Yeni Koronavirüs Hastalığı) Nedir?"
        embed.description = i["Nedir?"]

        for title in i["diger"]:
            embed.add_field(name=title, value=i["diger"][title], inline=False)

        embed.set_footer(text="T.C. Sağlık Bakanlığı")
        await ctx.send(embed=embed)

    @corona.command(name="about", aliases=["hakkında"])
    async def corona_api_about(self, ctx):
        """Kullanılan API hakkında bilgi verir."""

        async with ctx.typing():
            resp = await self.covid19.get_data()

        api_url = self.covid19.api_url
        source = self.covid19.source

        embed = discord.Embed(color=self.bot.embed_color)
        embed.title = f"COVID-19 API Hakkında"
        embed.description = (
            f"Durum: **`{resp.status} {resp.reason}`**\n"
            f"API adresi: [{api_url}]({api_url})\n"
            f"Kaynak kod: [{source}]({source})\n"
        )

        await ctx.send(embed=embed)

    # @commands.cooldown(1, 5, commands.BucketType.user)
    # @commands.command(aliases=["cvtr", "covid19tr"])
    async def coronatr(self, ctx):
        """Sağlık Bakanlığının hazırladığı Türkiye durumunu görüntüler."""

        url = "https://covid19.saglik.gov.tr/"

        embed = discord.Embed(color=self.bot.embed_color)
        embed.title = f"Türkiye'deki Güncel COVID-19 Durumu"
        embed.description = f"Kaynak: [{url}]({url})"

        async with ctx.typing():
            async with self.bot.session.get(url) as resp:
                resp = await resp.text()
            soup = BeautifulSoup(resp, "html.parser")

        div = soup.find_all("div", attrs={"class": "col-sm-12 col-xs-12 col-lg-6"})
        img1_url = url + div[0].find_all("img", attrs={"class": "img-fluid"})[0]["src"]
        img2_url = url + div[1].find_all("img", attrs={"class": "img-fluid"})[0]["src"]

        img1_bytes = await self.get_image_bytes(img1_url)
        img2_bytes = await self.get_image_bytes(img2_url)

        async with ctx.typing():
            img1 = Image.open(BytesIO(img1_bytes))
            img2 = Image.open(BytesIO(img2_bytes))

            img1_x, img1_y = img1.size
            img2_x, img2_y = img2.size
            size = (img1_x, img1_y + img2_y)
            bg = Image.new("RGB", size, "white")

            bg.paste(img1, (0, 0))
            bg.paste(img2, (0, img1_y))
            img1.close()
            img2.close()

            output_buffer = BytesIO()
            bg.save(output_buffer, "png")
            output_buffer.seek(0)

        file = discord.File(fp=output_buffer, filename="stats.png")
        embed.set_image(url="attachment://stats.png")

        await ctx.send(file=file, embed=embed)


def setup(bot):
    bot.add_cog(Info(bot))
