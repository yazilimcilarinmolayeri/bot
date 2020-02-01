# -*- coding: utf-8 -*-
#
# Copyright (C) 2019-2020, Yazılımcıların Mola Yeri (ymy-discord)
#

import emoji

from discord.utils import get


pong = "\U0001f3d3"


def unicode_to_name(e):
    return emoji.demojize(e.name)


def get(bot, name):
    return bot.get_emoji(get(bot.emojis, name=name).id)
