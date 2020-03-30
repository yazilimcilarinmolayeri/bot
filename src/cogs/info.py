# -*- coding: utf-8 -*-
#
# source/kaynak komutu kaynağı:
# - https://github.com/Rapptz/RoboDanny/blob/rewrite/cogs/meta.py#L328-L366
#

import os
import time
import json
import psutil
import aiohttp
import inspect
import humanize
import platform
import datetime
from PIL import Image
from io import BytesIO
from bs4 import BeautifulSoup

from .utils import http

import discord
from discord.ext import commands
from discord.utils import get


class Covid19:
    """COVID-19 API Sınıfı"""

    def __init__(self, bot):
        self.session = bot.session
        self.api_url = "https://covid19.mathdro.id/api"

    def _format(self, date_time):
        dt = datetime.datetime.strptime(date_time, "%Y-%m-%dT%H:%M:%S.%fZ").strftime(
            "%d.%m.%Y %H:%M:%S"
        )

        return dt

    async def get_data(self, params: str = "", res_method=None):
        async with self.session.get(self.api_url + params) as resp:
            if res_method == "json":
                return await resp.json()
            elif res_method == "text":
                return await resp.text()
            else:
                return resp

    async def last_update(self):
        r = await self.get_data(res_method="json")

        return self._format(r["lastUpdate"])

    async def get_global_stats(self):
        g = await self.get_data(res_method="json")

        g_stats = {}
        g_stats["confirmed"] = g["confirmed"]["value"]
        g_stats["recovered"] = g["recovered"]["value"]
        g_stats["deaths"] = g["deaths"]["value"]

        return g_stats

    async def get_countries(self):
        params = "/countries"
        countries = await self.get_data(params=params, res_method="json")

        return countries["countries"]

    async def get_country_stats(self, country):
        params = f"/countries/{country}"
        c = await self.get_data(params=params, res_method="json")
        
        c_stats = {}
        c_stats["confirmed"] = c["confirmed"]["value"]
        c_stats["recovered"] = c["recovered"]["value"]
        c_stats["deaths"] = c["deaths"]["value"]
        c_stats["lastUpdate"] = self._format(c["lastUpdate"])

        return c_stats

    async def get_top(self, limit=12):
        params = "/confirmed"
        confirmed = await self.get_data(params=params, res_method="json")

        return confirmed[0:limit]

    async def get_flag(country):
        pass


class Info(commands.Cog, name="Information"):
    """The description for Info goes here."""

    def __init__(self, bot):
        self.bot = bot
        self.covid19 = Covid19(bot)
        self.corona_image = "https://i.imgur.com/PZ5r1IB.png"
        self.reload_icon = "https://i.imgur.com/aouXufT.png"

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
                
        if country != None:
            command = self.bot.get_command("cv country")
            await command.__call__(ctx=ctx, country=country)
            return

        confirmed = global_stats["confirmed"]
        recovered = global_stats["recovered"]
        deaths = global_stats["deaths"]
        countries = await self.covid19.get_countries()

        mortality_rate = round((deaths / confirmed * 100), 2)
        recovery_rate = round((recovered / confirmed * 100), 2)

        embed = discord.Embed(color=self.bot.embed_color)
        embed.set_thumbnail(url=self.corona_image)
        embed.title = "COVID-19 Virüsü Global İstatistikleri"

        embed.add_field(name="Doğrulanan Vaka", value=f"{confirmed:,d}")
        embed.add_field(name="İyileşen Kişi", value=f"{recovered:,d}")
        embed.add_field(name="Ölen Kişi", value=f"{deaths:,d}")
        embed.add_field(name="Görülen Ülke", value=f"{len(countries):,d}")
        embed.add_field(name="İyileşme Oranı", value=f"{recovery_rate}%")
        embed.add_field(name="Ölüm Oranı", value=f"{mortality_rate}%")

        last_update = await self.covid19.last_update()
        embed.set_footer(text=f"Son güncelleme: {last_update}", icon_url=self.reload_icon)
        await ctx.send(embed=embed)

    @corona.command(name="countries", aliases=["ülkeler"])
    async def corona_countries(self, ctx):
        """Virüs bulunan ülkelerin bir listesini döndürür."""

        clist = {"1": "", "2": "", "3": ""}
        text = "1"
        async with ctx.typing():
            countries = await self.covid19.get_countries()
            for c in countries:
                if len(clist[text]) >= 1000:
                    text = str(int(text) + 1)
                else:
                    pass
                clist[text] += "`" + c["name"] + "`, "

        embed = discord.Embed(color=self.bot.embed_color)
        embed.description = f"Ülke istatistikleri için: `[corona/cv/covid19] [country_name]`"
        embed.title = f"COVID-19 Virüsü Bulunan Ülkeler ({len(countries)})"

        for v in clist:
            embed.add_field(name=f"Sayfa {v}", value=clist[v][0:-2], inline=False)
        
        # embed.set_footer(text="[corona/cv/covid19] [country_name]")
        await ctx.send(embed=embed)

    @corona.command(name="country", aliases=["ülke"])
    async def corona_country(self, ctx, country):
        """Verilen ülkenin virüs istatistiklerini görüntüler."""

        async with ctx.typing():
            country_stats = await self.covid19.get_country_stats(country)

        confirmed = country_stats["confirmed"]
        recovered = country_stats["recovered"]
        deaths = country_stats["deaths"]
        mortality_rate = round((deaths / confirmed * 100), 2)
        recovery_rate = round((recovered / confirmed * 100), 2)

        embed = discord.Embed(color=self.bot.embed_color)
        embed.set_thumbnail(url=self.corona_image)
        embed.title = f"COVID-19 Virüsü İstatistikleri ({country})"

        embed.add_field(name="Doğrulanan Vaka", value=f"{confirmed:,d}")
        embed.add_field(name="İyileşen Kişi", value=f"{recovered:,d}")
        embed.add_field(name="Ölen Kişi", value=f"{deaths:,d}")
        embed.add_field(name="İyileşme Oranı", value=f"{recovery_rate}%")
        embed.add_field(name="Ölüm Oranı", value=f"{mortality_rate}%")
        embed.add_field(name="\u200b", value="\u200b")

        embed.set_footer(text=f"Son güncelleme: {country_stats['lastUpdate']}", icon_url=self.reload_icon)
        await ctx.send(embed=embed)

    @corona.command(name="top", aliases=["üst"])
    async def corona_top(self, ctx):
        """Virüsden en çok etkilenen ülkeleri listeler."""

        async with ctx.typing():
            top = await self.covid19.get_top()

        embed = discord.Embed(color=self.bot.embed_color)
        embed.set_thumbnail(url=self.corona_image)
        embed.title = f"En Çok COVID-19 Virüslü Vaka Bulunan {(len(top))} Ülke"

        for country in top:
            country_region = country["countryRegion"]

            c = await self.covid19.get_country_stats(country_region)
            confirmed = c["confirmed"]
            recovered = c["recovered"]
            deaths = c["deaths"]

            value = f"Vaka: {confirmed:,d}\nÖlen: {recovered:,d}\nİyileşen: {deaths:,d}"
            embed.add_field(name=country_region, value=value)

        await ctx.send(embed=embed)

    @corona.command(name="global", aliases=["küresel"])
    async def corona_global(self, ctx):
        """Dünya geneli virüs istatistiklerini görsel olarak paylaşır."""
                
        embed = discord.Embed(color=self.bot.embed_color)
        embed.title = f"COVID-19 Virüsü Global İstatistik Grafiği"
        embed.set_image(url="https://covid19.mathdro.id/api/og")
        
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

        base_url = "https://covid19.mathdro.id/"
        source = "https://github.com/mathdroid/covid-19-api/"

        embed = discord.Embed(color=self.bot.embed_color)
        embed.title = f"COVID-19 API Hakkında"
        embed.description = (
            f"Durum: {resp.status} {resp.reason}\n"
            f"API adresi: [{base_url}]({base_url})\n"
            f"Kaynak kod: [{source}]({source})\n"
        )
        
        await ctx.send(embed=embed)

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(aliases=["cvtr", "covid19tr"])
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
