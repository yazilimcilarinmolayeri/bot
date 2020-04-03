# -*- coding: utf-8 -*-
#
# Yardımcı method ve fonksiyonlar...
#

from io import BytesIO
from collections import Counter
from PIL import Image, ImageDraw

import config

import discord


async def update_activity_name(bot):
    """Aktivite kısmına insan kullanıcı sayısını yazdırır."""

    guild = bot.get_guild(config.ymy_guild_id)
    # Bot miktarı True, bot olmayanların miktarı False anahtar isminde sayılır.
    # {"True": 0, "False": 0}
    human = Counter(str(m.bot) for m in guild.members)["False"]

    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching, name=f"{human:,d} üyeyi"
        )
    )


def draw_horizontal_chart(confirmed, recovered, deaths):
    """Vaka, iyileşen ve ölen kişilerin oranları hesaplayarak yatay bir grafik oluşturur."""

    margin = 25
    mh = margin / 2
    w, h = (500 - margin, 40 - margin)

    gold = (241, 196, 15)  # f1c40f
    green = (46, 204, 113)  # 2ecc71
    red = (231, 76, 60)  # e74c3c

    total = confirmed + recovered + deaths
    case_rate = confirmed / total * w
    recovery_rate = recovered / total * w
    mortality_rate = deaths / total * w

    img = Image.new("RGB", (w + margin, h + margin), (47, 49, 54))
    draw = ImageDraw.Draw(img)

    x = case_rate + mh
    y = recovery_rate + x
    z = mortality_rate + y

    draw.rectangle((mh, mh, x, h + mh), fill=gold)
    draw.rectangle((x, mh, y, h + mh), fill=green)
    draw.rectangle((y, mh, z, h + mh), fill=red)

    output_buffer = BytesIO()
    img.save(output_buffer, "png")
    output_buffer.seek(0)

    return output_buffer
