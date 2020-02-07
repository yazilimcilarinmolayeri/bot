# -*- coding: utf-8 -*-
#

from os import listdir, environ


"""
GNU/Linux'da sistem değişkeni oluşturmak için yapmanız gerekenler:
  Ev dizinize gidin.
    $ cd ~
  Ev dizinindeki .bashrc dosyasını düzenlemek için bir editör ile açın.
    $ nano .bashrc
  Dosyaya şunları ekleyin ve kaydedip çıkın.
    TOKEN='TOKEN ANAHTARI'
    export TOKEN
  Daha sonra şu komutu çalıştırın.
    $ source .bashrc
  İşlem tamamdır, sistem değişkeni kullanılabilir durumda.
"""

token = environ.get('TOKEN')

# 
# Sistem değişkeni oluşturmak istemiyorsanız alttaki token değişkekine
# bot tokenini yazınız...
#

if token == None:
    token = 'TOKEN'

#
# Yazılımcıların Mola Yeri için özel değişkenler. Değişkenler dinamik 
# üretilecek şekilde olması için daha sonra bu kodlara el atılacak.
# 

ymy_guild_id = 418887354699350028

# Reaksiyon ile rol almak için kullanılan kanal ve mesaj değişkenleri.

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
