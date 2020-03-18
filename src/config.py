# -*- coding: utf-8 -*-
#

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
    "+", "ymy+",
]

owner_ids = [
    428273380844765185, 
    335119989893890049, 
    429276634072350720,
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
beni_oku_message_id = 641621615238578207

reaction_role_channel_id = 485084529443471390
reaction_role_message_ids = [
    626720184425644033,
    626720225215250433,
    626720265979822110,
    626720296631664640,
    626720397173325825,
    626720468136755200,
    626720493776404502,
    626720518720192585,
    626720542736777217,
]
