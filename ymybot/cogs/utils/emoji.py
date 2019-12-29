# -*- coding: utf-8 -*-
#
# Copyright (C) 2019, Yazılımcıların Mola Yeri (ymy-gitrepo)
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

import emoji

from discord.utils import get


pong = "\U0001f3d3"


def unicode_to_name(e):
    return emoji.demojize(e.name)


def get(bot, name):
    return bot.get_emoji(get(bot.emojis, name=name).id)
