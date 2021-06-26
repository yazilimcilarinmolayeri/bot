# -*- coding: utf-8 -*-

from os import environ as env
from ast import literal_eval as le


#
# GNU/Linux'da sistem değişkeni oluşturmak için yapmanız gerekenler:
# 1. Ev dizinize gidin.
#   $ cd ~
# 2. Ev dizinindeki .bashrc dosyasını düzenlemek için bir editör ile açın.
#   $ nano .bashrc
# 3. Dosyaya şunları ekleyin ve kaydedip çıkın.
#   token='token'
#   export token
# 4. Daha sonra şu komutu çalıştırın.
#   $ source .bashrc
#
# İşlem tamam, sistem değişkeni kullanılabilir durumda. Test etmek için:
#   $ echo $token
#

token = env.get("token")

prefix = [
    "+",
    "ymy ",
    "ymy+",
]

owner_ids = [
    428273380844765185,
    335119989893890049,
    429276634072350720,
    666581334637936640,
    668800516448452630,
]

#
# imgflip.com
#
# {"username": "", "password": ""}
imgflip_api = le(env.get("imgflip_api"))

#
# screenshotapi.net
#
# {"token": ""}
screenshot_api = le(env.get("screenshot_api"))


# ============================Yazılımcıların Mola Yeri============================

#
# Yazılımcıların Mola Yeri (YMY) için özel değişkenler. Değişkenler dinamik
# üretilecek şekilde olması için daha sonra bu kodlara el atılacak.
#

ymy_guild_id = 418887354699350028

#
# Reaksiyon ile rol almak için kullanılan kanal ve mesaj değişkenleri.
#

beni_oku_channel_id = 609350584314626049
beni_oku_message_id = 428273380844765185

rr_channel_id = 485084529443471390
rr_role_message_ids = [
    690869405676077057,
    690869406623989790,
    690869407253266454,
    690869408108773427,
    690869408884719617,
    690869427624738826,
    690869428308672572,
    690869429042675732,
    690869429747318814,
    690869430334259241,
]
