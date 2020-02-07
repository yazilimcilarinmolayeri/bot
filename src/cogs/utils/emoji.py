# -*- coding: utf-8 -*-
#

import emoji

from discord.utils import get


def unicode_to_name(e):
    return emoji.demojize(e.name)


def get(bot, name):
    return bot.get_emoji(get(bot.emojis, name=name).id)
