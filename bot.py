# By Casper 👻
#    Copyright (c) 2021-2022 Casper
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, version 3.
#
#    This program is distributed in the hope that it will be useful, but
#    WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
#    General Public License for more details.
#
#    License can be found in < https://github.com/suphiozturk8/ChannelAutoPost/blob/main/License> .

import logging
from telethon import TelegramClient, events, Button
from decouple import config

logging.basicConfig(
    format="[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s", level=logging.INFO
)

# start the bot
logging.info("👻 Bot Başlatılıyor...")
try:
    apiid = config("APP_ID", cast=int)
    apihash = config("API_HASH")
    bottoken = config("BOT_TOKEN")
    frm = config("FROM_CHANNEL", cast=lambda x: [int(_) for _ in x.split(" ")])
    tochnls = config("TO_CHANNEL", cast=lambda x: [int(_) for _ in x.split(" ")])
    casper = TelegramClient("bot", apiid, apihash).start(bot_token=bottoken)
except:
    logging.error("👻 Ortam değişkenleri eksik! Lütfen tekrar kontrol edin ✘")
    logging.info("👻 Bot durduruldu ✘")
    exit()


@casper.on(events.NewMessage(pattern="/start"))
async def _(event):
    await event.reply(
        f"**Merhaba {event.sender.first_name} 👻\n\nBen bir otomatik gönderi botuyum.\n\nDaha fazlasını öğrenmek için /help tıklayınız.\n\nAynı anda sadece iki kanalda (bir kullanıcı) kullanılabilir.\nLütfen kendi botunuzu kurun.**", 
        buttons=(
        [
            Button.url("👻 Repo", url="https://github.com/suphiozturk8/ChannelAutoPost"),
            Button.url("👻 Sahip", url="https://t.me/Suphi_Casper"),
        ],
        [
            Button.url("👻 Diyer Botlarım", url="https://t.me/BioCasper/42"),
        ],
        )
        ,link_preview=False,
    )

@casper.on(events.NewMessage(pattern="/help"))
async def helpp(event):
    await event.reply(
        "**👻                Yardım                👻\n\nBu bot, bir kanaldaki tüm yeni gönderileri diğer bir kanala gönderebilir.\n(yönlendirilen etiketi olmadan)\n\nAynı anda yalnızca iki kanalda kullanılabilir, bu yüzden lütfen kendi botunuzu kurun.\n\nBotu her iki kanala da ekleyin ve yönetici yapın, böylece tüm yeni mesajlar bağlı kanalda otomatik olarak yayınlanır.**",
       buttons=[
         Button.url("Botu Ekle ➕", url="http://t.me/Casper_AutoPost_Bot?startgroup=new&startchannel=new"),
           ],
        link_preview=False,
    )


@casper.on(events.NewMessage(incoming=True, chats=frm))
async def _(event):
    for tochnl in tochnls:
        try:
            if event.poll:
                return
            if event.photo:
                photo = event.media.photo
                await casper.send_file(
                    tochnl, photo, caption=event.text, link_preview=False
                )
            elif event.media:
                try:
                    if event.media.webpage:
                        await casper.send_message(
                            tochnl, event.text, link_preview=False
                        )
                except Exception:
                    media = event.media.document
                    await casper.send_file(
                        tochnl, media, caption=event.text, link_preview=False
                    )
                finally:
                    return
            else:
                await casper.send_message(tochnl, event.text, link_preview=False)
        except Exception as exc:
            logging.error(
                "TO_CHANNEL Kimliği yanlış veya oraya mesaj gönderemiyorum (beni yönetici yapmayı dene).\nGeri izleme:%s",
                exc,
            )


logging.info("👻 Bot başlatıldı ✓")
logging.info("@BioCasper ziyaret edin 👻")
casper.run_until_disconnected()
