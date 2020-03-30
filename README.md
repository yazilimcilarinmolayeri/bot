# :robot: YMYBot

<p>
  <img src="https://img.shields.io/discord/418887354699350028?style=flat">
  <img src="https://img.shields.io/badge/python-3.7-blue">
  <img src="https://img.shields.io/badge/discord-py-blue">
  <img src="https://img.shields.io/badge/code%20style-black-black">
</p>

YMY (Yazılımcıların Mola Yeri) geliştiricileri tarafından sunucu ihtiyaçları için yazılmış bot.

### Ön koşullar
* Python versiyonu 3.7 veya daha yüksek olmalı

## Yükleme
```
git clone https://github.com/ymyoh/ymybot
```

## Kurulum
Sanal geliştirme ortamının kurulma amacı, pip ile kurduğunuz paketlerin bilgisayarınıza değil sadece bu proje dosyaları içersinedeki sanal ortama yükleniyor olmasıdır. Projenizi sildiğinizde de paketler silinmiş olur. Sanal geliştirme ortamı kurmak istemeyenler 1,2 ve 4. adımı atlayabilirler.

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
python3.7 src/bot.py
```

## Katkı ve Test
Düzenleniyor...

## Kütüphaneler
* [emoji](https://github.com/carpedm20/emoji)
* [arrow](https://github.com/crsmithdev/arrow)
* [psutil](https://github.com/giampaolo/psutil)
* [Pillow](https://github.com/python-pillow/Pillow)
* [jishaku](https://github.com/Gorialis/jishaku)
* [humanize](https://github.com/jmoiron/humanize)
* [discord.py](https://github.com/Rapptz/discord.py)
* [beautifulsoup4](https://code.launchpad.net/beautifulsoup)

## Bağlantılar
Projeyi test etmek, hakkında merak ettiklerini öğrenmek için [destek](https://discord.gg/KazHgb2) sunucusuna katıl.

## Lisans
[GPL 3.0](LICENSE) © **Yazılımcıların Mola Yeri**
