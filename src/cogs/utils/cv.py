# -*- coding: utf-8 -*-
#
# YMYBot Copyright (C) 2019-2020 Yazılımcıların Mola Yeri (ymyoh)
# COVID-19 API Crawler
#

from datetime import datetime

from cogs.utils import http


class Covid19:
    """COVID-19 API Sınıfı"""

    gold = "<:gold:694666442913611847>"
    green = "<:green:694666519174578176>"
    red = "<:red:694666443215863838>"

    image = "https://covid19.mathdro.id/api/og"
    corona_image = "https://i.imgur.com/PZ5r1IB.png"
    reload_icon = "https://i.imgur.com/JoPA7l8.png"

    def __init__(self, bot):
        self.session = bot.session
        self.api_url = "https://covid19.mathdro.id/api"
        self.source = "https://github.com/mathdroid/covid-19-api"

    def _format(self, date_time):
        """Tarih ve saati Türkçe kurallarına uygun şekilde okunabilir hale getirir."""

        dt = datetime.strptime(date_time, "%Y-%m-%dT%H:%M:%S.%fZ").strftime(
            "%d.%m.%Y %H:%M:%S"
        )

        return dt

    async def get_data(self, params: str = "", res_method=None):
        """API'ye verilen parametrleri istek oluşturur ve gelen istekleri döndürür."""

        async with self.session.get(self.api_url + params) as resp:
            if res_method == "json":
                return await resp.json()
            elif res_method == "text":
                return await resp.text()
            else:
                return resp

    async def last_update(self):
        """Küresel verilerin son güncellenme tarihini döndürür."""

        r = await self.get_data(res_method="json")

        return self._format(r["lastUpdate"])

    async def get_global_stats(self):
        """Küresel vaka, iyleşme ve ölüm sayılarını verir."""

        _global = await self.get_data(res_method="json")

        gstats = {}
        gstats["confirmed"] = _global["confirmed"]["value"]
        gstats["recovered"] = _global["recovered"]["value"]
        gstats["deaths"] = _global["deaths"]["value"]

        return gstats
                    
    async def get_countries(self):
        """Virüs bulunan üleklerinin isim listesini döndürür."""

        params = "/countries"
        countries = await self.get_data(params=params, res_method="json")

        country_list = []

        for country in countries["countries"]:
            try:
                country_list.append(
                    [country["name"], country["iso2"], country["iso3"],]
                )
            except KeyError:
                country_list.append([country["name"]])

        return country_list

    async def get_country_stats(self, country):
        """Verilen ülkenin vaka, iyleşme ve ölüm sayılarını verir."""

        params = f"/countries/{country}"
        country = await self.get_data(params=params, res_method="json")

        cstats = {}
        cstats["confirmed"] = country["confirmed"]["value"]
        cstats["recovered"] = country["recovered"]["value"]
        cstats["deaths"] = country["deaths"]["value"]
        cstats["lastUpdate"] = self._format(country["lastUpdate"])

        return cstats

    async def get_top(self, limit=12):
        """Limit sayı dahilinde en çok vaka bulunan ülkeleri döndürür."""

        country_top_list = []

        class CountryStats:
            country_region = ""
            flag = ""
            confirmed = 0
            recovered = 0
            deaths = 0

        params = "/confirmed"
        confirmed = await self.get_data(params=params, res_method="json")

        for country in confirmed[0:limit]:
            country_region = country["countryRegion"]

            stats = CountryStats()
            cstats = await self.get_country_stats(country_region)

            stats.country_region = country_region
            stats.flag = await self.get_flag(country_region)
            stats.confirmed = cstats["confirmed"]
            stats.recovered = cstats["recovered"]
            stats.deaths = cstats["deaths"]

            country_top_list.append(stats)

        return country_top_list

    async def country_name_check(self, country_name):
        """Verilen ülke ad veya kodunun doğru olup olmadığına bakar."""

        status = [False, []]
        countries = await self.get_countries()

        for names in countries:
            for name in names:
                if country_name.lower() == name.lower():
                    status[0] = True
                    
                    try:
                        status[1] = names
                    except KeyError:
                        status[1] = names[0]

                    return status
                
        return status

    async def get_flag(self, country_name):
        """Verilen ülkenin bayrağını emoji olarak döndürür."""

        check = await self.country_name_check(country_name)

        if check[0]:
            return f":flag_{check[1][1].lower()}:"
        else:
            pass
