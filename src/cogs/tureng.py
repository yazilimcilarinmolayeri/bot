import aiohttp
import asyncio
from bs4 import BeautifulSoup as bs

import discord
from discord.ext import commands


class Tureng(commands.Cog):
    def __init__(self, bot):
        self.client = bot

    @commands.command()
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def tureng(self, ctx, language, *, word):
        """
        Türkçe-İngilizce sözlük komutu.
        
        Örnek:
            ymy+tureng en_tr query
            ymy+tureng tr_en sorgu
        
        Geliştirici: Emir Kılıçaslan (realjtr) <<https://github.com/realJtr>>
        """

        async with aiohttp.ClientSession() as cs:
            async with cs.get(f"https://tureng.com/tr/turkce-ingilizce/{word}") as resp:
                text = await resp.read()

            soup = bs(text.decode("utf-8", "html.parser"))

        if soup.find("h1").text == "Sanırız yanlış oldu, doğrusu şunlar olabilir mi?":
            await ctx.send(f"{word}, diye bir kelime bulamadım.")
        else:
            # We want to find out which language our user wants to translate from to provide some misunderstanding
            if language == "en_tr":

                content = []
                tables = soup.find_all(
                    "table",
                    {"class": "table table-hover table-striped searchResultsTable"},
                )
                c2 = tables[0].find_all("tr")[0].find_all("th", {"class": "c2"})
                c2_text = c2[0].text
                # detect what is in the first table
                if c2_text == "İngilizce":

                    table_tr = tables[0].find_all("tr")
                    x = len(table_tr)
                    # algorithm that find the words.
                    for i in range(3, x):
                        category = table_tr[i].find_all("td", {"class": "hidden-xs"})

                        a = table_tr[i].find_all("a")

                        if len(a) == 0 and len(category) == 0:
                            pass
                        else:
                            content.append(f"{category[1].text}$${a[1].text}")

                            # embed.add_field(name=f"{category[1].text}", value=f"{a[1].text}", inline=False)
                            # print(f'{category[1].text} - {a[1].text}')
                else:
                    table_tr = tables[1].find_all("tr")
                    x = len(table_tr)
                    for i in range(3, x):
                        category = table_tr[i].find_all("td", {"class": "hidden-xs"})
                        a = table_tr[i].find_all("a")

                        if len(a) == 0 and len(category) == 0:
                            pass
                        else:
                            content.append(f"{category[1].text}$${a[1].text}")

                            # embed.add_field(name=f"{category[1].text}", value=f"{a[1].text}", inline=False)

                            # print(f'{category[1].text} - {a[1].text}'

                def check(reaction, user):
                    return user == ctx.author and str(reaction.emoji) in ["◀️", "▶️"]
                    # This makes sure nobody except the command sender can interact with the "menu"

                x = len(content)
                # calculate how much pages will be
                if float(x / 5) > int(x / 5):
                    pages = int(x / 5) + 1

                else:
                    pages = int((x / 5))

                cur_page = 1
                a = 0
                b = 5

                embed = discord.Embed(
                    colour=self.client.embed_color,
                    title=f"Kelime: {word}",
                    description="İngilizce -> Türkçe",
                )
                embed.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
                # if there is only one page avoid from the index error.
                if x <= 5:
                    for word in range(a, x):
                        category, text = content[word].split("$$")
                        embed.add_field(
                            name=f"{category}", value=f"{text}", inline=False
                        )
                        embed.set_footer(
                            text=f"Kelime Sayısı: {x}\nSayfa Sayısı: 1/{pages}\n"
                        )

                    await ctx.send(embed=embed)

                else:
                    for word in range(a, b):
                        category, text = content[word].split("$$")
                        embed.add_field(
                            name=f"{category}", value=f"{text}", inline=False
                        )
                    # showing the what is the page right now and how much word there is
                    embed.set_footer(
                        text=f"Kelime Sayısı: {x}\nSayfa Sayısı: {cur_page}/{pages}"
                    )

                    message = await ctx.send(embed=embed)
                    await message.add_reaction("◀️")
                    await message.add_reaction("▶️")

                    while True:

                        try:
                            reaction, user = await self.client.wait_for(
                                "reaction_add", timeout=30, check=check
                            )
                            # waiting for a reaction to be added - times out after x seconds, 60 in this
                            # example

                            if str(reaction.emoji) == "▶️" and cur_page < pages:

                                cur_page += 1

                                a += 5
                                b += 5
                                if cur_page == pages:
                                    counter = 0
                                    excess = 5 - (x - a)
                                    # when it comes to last page there is some word from previous and we must the detect them and delete.
                                    if excess < 5:

                                        for delete in range(1, excess + 1):

                                            embed.remove_field(-delete)

                                    for word in range(a, x):

                                        category, text = content[word].split("$$")
                                        # embed.add_field(name=f"{category}", value=f"{text}", inline=False)
                                        embed.set_field_at(
                                            counter,
                                            name=f"{category}",
                                            value=f"{text}",
                                            inline=False,
                                        )
                                        counter += 1
                                        embed.set_footer(
                                            text=f"Kelime Sayısı: {x}\nSayfa Sayısı: {cur_page}/{pages}"
                                        )

                                    await message.edit(embed=embed)
                                    await message.remove_reaction(reaction, user)
                                else:
                                    counter = 0
                                    for word in range(a, b):
                                        category, text = content[word].split("$$")
                                        embed.set_field_at(
                                            counter,
                                            name=f"{category}",
                                            value=f"{text}",
                                            inline=False,
                                        )
                                        counter += 1
                                        embed.set_footer(
                                            text=f"Kelime Sayısı: {x}\nSayfa Sayısı: {cur_page}/{pages}"
                                        )

                                    await message.edit(embed=embed)
                                    await message.remove_reaction(reaction, user)

                            elif str(reaction.emoji) == "◀️" and cur_page > 1:

                                counter = 0
                                cur_page -= 1
                                a -= 5
                                b -= 5
                                embed.clear_fields()
                                for word in range(a, b):

                                    category, text = content[word].split("$$")
                                    # embed.add_field(name=f"{category}", value=f"{text}", inline=False)
                                    # embed.set_field_at(counter, name=f"{category}", value=f"{text}", inline=False)

                                    embed.insert_field_at(
                                        counter,
                                        name=f"{category}",
                                        value=f"{text}",
                                        inline=False,
                                    )
                                    counter += 1
                                    embed.set_footer(
                                        text=f"Kelime Sayısı: {x}\nSayfa Sayısı: {cur_page}/{pages}"
                                    )

                                await message.edit(embed=embed)

                                await message.remove_reaction(reaction, user)

                            else:

                                await message.remove_reaction(reaction, user)
                                # removes reactions if the user tries to go forward on the last page or
                                # backwards on the first page
                        except asyncio.TimeoutError:

                            await message.delete()
                            break
                            # ending the loop if user doesn't react after x seconds

            elif language == "tr_en":

                content = []
                tables = soup.find_all(
                    "table",
                    {"class": "table table-hover table-striped searchResultsTable"},
                )
                c2 = tables[0].find_all("tr")[0].find_all("th", {"class": "c2"})
                c2_text = c2[0].text
                if c2_text == "Türkçe":

                    table_tr = tables[0].find_all("tr")
                    x = len(table_tr)
                    for i in range(3, x):
                        category = table_tr[i].find_all("td", {"class": "hidden-xs"})

                        a = table_tr[i].find_all("a")

                        if len(a) == 0 and len(category) == 0:
                            pass
                        else:
                            content.append(f"{category[1].text}$${a[1].text}")

                            # embed.add_field(name=f"{category[1].text}", value=f"{a[1].text}", inline=False)
                            # print(f'{category[1].text} - {a[1].text}')
                else:
                    table_tr = tables[1].find_all("tr")
                    x = len(table_tr)
                    for i in range(3, x):
                        category = table_tr[i].find_all("td", {"class": "hidden-xs"})
                        a = table_tr[i].find_all("a")

                        if len(a) == 0 and len(category) == 0:
                            pass
                        else:
                            content.append(f"{category[1].text}$${a[1].text}")

                            # embed.add_field(name=f"{category[1].text}", value=f"{a[1].text}", inline=False)

                            # print(f'{category[1].text} - {a[1].text}')

                def check(reaction, user):
                    return user == ctx.author and str(reaction.emoji) in ["◀️", "▶️"]
                    # This makes sure nobody except the command sender can interact with the "menu"

                x = len(content)

                if float(x / 5) > int(x / 5):
                    pages = int(x / 5) + 1

                else:
                    pages = int((x / 5))

                cur_page = 1
                a = 0
                b = 5

                embed = discord.Embed(
                    colour=self.client.embed_color,
                    title=f"Kelime: {word}",
                    description="Türkçe -> İngilizce",
                )

                if x <= 5:
                    for word in range(a, x):
                        category, text = content[word].split("$$")
                        embed.add_field(
                            name=f"{category}", value=f"{text}", inline=False
                        )
                        embed.set_footer(
                            text=f"Kelime Sayısı: {x}\nSayfa Sayısı: 1/{pages}"
                        )
                    await ctx.send(embed=embed)

                else:
                    for word in range(a, b):
                        category, text = content[word].split("$$")
                        embed.add_field(
                            name=f"{category}", value=f"{text}", inline=False
                        )
                        embed.set_footer(
                            text=f"Kelime Sayısı: {x}\nSayfa Sayısı: {cur_page}/{pages}"
                        )

                    message = await ctx.send(embed=embed)
                    await message.add_reaction("◀️")
                    await message.add_reaction("▶️")

                    while True:

                        try:
                            reaction, user = await self.client.wait_for(
                                "reaction_add", timeout=60, check=check
                            )
                            # waiting for a reaction to be added - times out after x seconds, 60 in this
                            # example

                            if str(reaction.emoji) == "▶️" and cur_page < pages:

                                cur_page += 1

                                a += 5
                                b += 5
                                if cur_page == pages:
                                    counter = 0
                                    excess = 5 - (x - a)
                                    if excess < 5:

                                        for delete in range(1, excess + 1):
                                            # 10 13  => 5-3 = 2 tane fazlalık var demektir.
                                            # 2

                                            embed.remove_field(-delete)

                                    for word in range(a, x):
                                        category, text = content[word].split("$$")
                                        # embed.add_field(name=f"{category}", value=f"{text}", inline=False)
                                        embed.set_field_at(
                                            counter,
                                            name=f"{category}",
                                            value=f"{text}",
                                            inline=False,
                                        )
                                        counter += 1
                                        embed.set_footer(
                                            text=f"Kelime Sayısı: {x}\nSayfa Sayısı: {cur_page}/{pages}"
                                        )

                                    await message.edit(embed=embed)
                                    await message.remove_reaction(reaction, user)
                                else:
                                    counter = 0
                                    for word in range(a, b):
                                        category, text = content[word].split("$$")
                                        embed.set_field_at(
                                            counter,
                                            name=f"{category}",
                                            value=f"{text}",
                                            inline=False,
                                        )
                                        counter += 1
                                        embed.set_footer(
                                            text=f"Kelime Sayısı: {x}\nSayfa Sayısı: {cur_page}/{pages}"
                                        )

                                    await message.edit(embed=embed)
                                    await message.remove_reaction(reaction, user)

                            elif str(reaction.emoji) == "◀️" and cur_page > 1:

                                counter = 0
                                cur_page -= 1
                                a -= 5
                                b -= 5
                                embed.clear_fields()
                                for word in range(a, b):
                                    category, text = content[word].split("$$")
                                    # embed.add_field(name=f"{category}", value=f"{text}", inline=False)
                                    # embed.set_field_at(counter, name=f"{category}", value=f"{text}", inline=False)

                                    embed.insert_field_at(
                                        counter,
                                        name=f"{category}",
                                        value=f"{text}",
                                        inline=False,
                                    )
                                    counter += 1
                                    embed.set_footer(
                                        text=f"Kelime Sayısı: {x}\nSayfa Sayısı: {cur_page}/{pages}"
                                    )

                                await message.edit(embed=embed)

                                await message.remove_reaction(reaction, user)

                            else:

                                await message.remove_reaction(reaction, user)
                                # removes reactions if the user tries to go forward on the last page or
                                # backwards on the first page
                        except asyncio.TimeoutError:

                            await message.delete()
                            break
                            # ending the loop if user doesn't react after x seconds


def setup(bot):
    bot.add_cog(Tureng(bot))
