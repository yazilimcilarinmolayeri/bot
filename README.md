# :robot: YMYBot

<p>
  <img src="https://img.shields.io/badge/python-3.7-blue">
  <img src="https://img.shields.io/badge/discord-py-blue">
  <img src="https://img.shields.io/badge/code%20style-black-black">
  <img src="https://img.shields.io/discord/418887354699350028?style=flat">
</p>

YMY (Yazılımcıların Mola Yeri) geliştiricileri tarafından sunucu ihtiyaçları için yazılmış Discord bot'u. Projeyi test etmek, hakkında merak ettiklerini öğrenmek için [destek](https://discord.gg/KazHgb2) sunucusuna katıl.

> **UYARI/WARNING** <br/>
> Bu bot artık aktif olarak geliştirilmemektedir, lütfen ymybot-rw botuna pr atın. <br/>
> This bot isn't under develop anymore, please send your pr's to ymybot-rw.

<!-- <img src="https://i.imgur.com/6yTRFq1.gif"/> -->

## Gereksinimler
* Python versiyonu 3.7 veya daha yüksek olmalı.

## Kurulum
Sanal geliştirme ortamının kurulma amacı, pip ile kurduğunuz paketlerin bilgisayarınıza değil sadece bu proje dosyaları içersinedeki sanal ortama yükleniyor olmasıdır. Projenizi sildiğinizde de paketler silinmiş olur. Sanal geliştirme ortamı kurmak istemeyenler 1,2 ve 4. adımı atlayabilirler.

1. Depoyu klonla:
```
$ git clone https://github.com/ymyoh/ymybot
```

2. Sanal geliştirme ortamı hazırla:
```
$ cd ymybot
$ virtualenv --python=/usr/bin/python3.7 .venv
```

3. Geliştirme ortamını aktif et:
```
$ source .venv/bin/activate
```

4. Proje bağımlıklarını yükle:
```
$ pip3 install -U -r requirements.txt
```

5. Geliştirme ortamından çık:
```
$ deactivate
```

6. Bot için gerekli ayarları yap:
[config.py](https://github.com/ymy-discord/ymybot/blob/master/src/config.py) dosyasını herhangi bir metin düzenleyicisi ile açarak `token = "TOKEN"` değişkenini ayarla.

7. Projeyi çalıştır:
```
$ python3.7 src/bot.py
```

## Lisans
[GPL 3.0](LICENSE) © **Yazılımcıların Mola Yeri**
