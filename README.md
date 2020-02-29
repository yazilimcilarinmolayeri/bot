# :robot: YMYBot

<p>
  <img src="https://img.shields.io/discord/418887354699350028?style=flat">
  <img src="https://img.shields.io/badge/python-3.7-blue">
  <img src="https://img.shields.io/badge/discord-py-blue">
  <img src="https://img.shields.io/badge/code%20style-black-black">
</p>

YMY (Yazılımcıların Mola Yeri) geliştiricileri tarafından sunucu ihtiyaçları için yazılmış bot.

### Önkoşullar
* Python versiyonu 3.7 veya daha yüksek olmalı

## Yükleme
```
git clone https://github.com/ymy-discord/ymybot
```

## Kurulum
Sanal geliştirme ortamının kurulma amacı, pip ile kurduğunuz paketlerin bilgisayarınıza değil sadece bu proje dosyaları içersinedeki sanal ortama yükleniyor olmasıdır. Projenizi sildiğinizde de paketler silinmiş olur. Sanal geliştirme ortamı kurmak istemeyenler sadece 3. adımı uygulasınlar.

1. Sanal geliştirme ortamı hazırla

```
cd ymybot
virtualenv --python=/usr/bin/python3.7 .venv
```

2. Geliştirme ortamını aktif et

```
source .venv/bin/activate
```

3. Proje bağımlıklarını yükle

```
pip3 install -U -r requirements.txt
```

4. Geliştirme ortamından çık

```
deactivate
```

5. Bot için gerekli ayarları yap

[config.py](https://github.com/ymy-discord/ymybot/blob/master/src/config.py) dosyasını herhangi bir metin düzenleyicisi ile açarak `token = "TOKEN"` değişkenini ayarla.

6. Projeyi çalıştır

```
cd src
python3.7 bot.py
```

## Katkı ve Test
Düzenleniyor...

## Kütüphaneler
* [emoji](https://github.com/carpedm20/emoji)
* [jishaku](https://github.com/Gorialis/jishaku)
* [discord.py](https://github.com/Rapptz/discord.py)

## Lisans
[GPL 3.0](LICENSE) © **Yazılımcıların Mola Yeri**
