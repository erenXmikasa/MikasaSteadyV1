import yt_dlp
from pyrogram import filters
from pyrogram import Client
from Music import (
    dbb, 
    app,
    SUDOERS,
    BOT_NAME,
    BOT_ID,
    BOT_USERNAME,
    OWNER,
)
from Music.MusicUtilities.helpers.inline import start_keyboard, personal_markup
from Music.MusicUtilities.helpers.thumbnails import down_thumb
from Music.MusicUtilities.tgcallsrun.prime import user
from Music.MusicUtilities.helpers.ytdl import ytdl_opts 
from Music.MusicUtilities.helpers.filters import command
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InputMediaPhoto,
    Message,
)
from Music.MusicUtilities.database.chats import (get_served_chats, is_served_chat, add_served_chat, get_served_chats)
from Music.MusicUtilities.database.queue import (is_active_chat, add_active_chat, remove_active_chat, music_on, is_music_playing, music_off)
from Music.MusicUtilities.database.sudo import (get_sudoers, get_sudoers, remove_sudo)

pstart_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        f"➕ Tambahkan Ke Group ➕", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")
                ],[
                    InlineKeyboardButton(
                        "📣 Channel", url="https://t.me/vecekayehhh"), 
                    InlineKeyboardButton(
                        "👥 Group", url="https://t.me/virtualmutualangroup")
                ],[
                    InlineKeyboardButton(
                        "🎉 Creator", url="https://t.me/vckyclone")
                ]
            ]
        ) 


@Client.on_message(filters.group & filters.command(["start"]))
async def musicstart(_, message: Message):
    chat_id = message.chat.id
    await message.reply_text(
        f"""❂Hai {message.from_user.mention()}!

Terima kasih telah menggunakan Saya Di {message.chat.title}.
Untuk bantuan atau bantuan apa pun, Silahkan Chat Owner Atau Join grup kami.""",
       reply_markup=pstart_markup,
       disable_web_page_preview=True
    )

@Client.on_message(filters.group & filters.command(["help"]))
async def ghelp(_, message: Message):
    await message.reply_text(
        f"""🕵🏼‍♂️ Perintah dasar:
» /play (nama lagu/tautan) - putar musik di obrolan suara
» /videostream (kata kunci/tautan) - streaming yt live/radio video music
» /videoplay (kata kunci/tautan video) - putar video di obrolan suara
» /playlist - Menunjukan daftar putar
» /video (kata kunci) - Unduh video
» /song (kata kunci) - Unduh lagu
» /lyric (kata kunci) - Mencari lirik lagu
» /search (kata kunci) - Cari link video
» /ping - tampilkan status ping robot
» /info - tampilkan info robot aktif (dalam grup)

👮🏼‍♂️ Perintah admin:
» /pause - jeda streaming
» /resume - lanjutkan streaming
» /skip - beralih ke aliran berikutnya
» /end - hentikan streaming
» /mute - bisukan robot pengguna di obrolan suara
» /unmute - mengaktifkan suara robot pengguna di obrolan suara
» /volume 1-200 - mengatur volume musik (pengguna robot harus admin)
» /reload - memuat ulang robot dan daftar admin
» /userbotjoin - undang pengguna robot untuk bergabung dengan grup
» /userbotleave - perintahkan pengguna robot keluar dari grup

👷🏼‍♂️ Perintah sudo (asisten):
» /rmw - Bersihkan semua file mentah
» /rmd - Bersihkan semua file yang diunduh
» /leaveall - Perintahkan pengguna robot keluar dari semua grup
» /playmusic on/off - Perintahkan pengguna robot bisa memutar musik atau tidak
» /usage - Melihat sisa dyno
» /uptime - tampilkan status waktu aktif robot
» /usage - tampilkan status waktu aktif robot
» /cpu - tampilkan prosesor yang digunakan robot""",
    )
    
@Client.on_message(filters.private & filters.incoming & filters.command("start"))
async def play(_, message: Message):
    if len(message.command) == 1:
        user_id = message.from_user.id
        user_name = message.from_user.first_name
        rpk = "["+user_name+"](tg://user?id="+str(user_id)+")" 
        await app.send_message(message.chat.id,
            text=f"❂Hai. {rpk}!\n[❂](https://telegra.ph/file/add31c6018ba67309bd3b.jpg)Saya Dapat memutar musik di Obrolan Suara Telegram.",
            parse_mode="markdown",
            reply_markup=pstart_markup
        )
    elif len(message.command) == 2:                                                           
        query = message.text.split(None, 1)[1]
        f1 = (query[0])
        f2 = (query[1])
        f3 = (query[2])
        finxx = (f"{f1}{f2}{f3}")
        if str(finxx) == "inf":
            query = ((str(query)).replace("info_","", 1))
            query = (f"https://www.youtube.com/watch?v={query}")
            with yt_dlp.YoutubeDL(ytdl_opts) as ytdl:
                x = ytdl.extract_info(query, download=False)
            thumbnail = (x["thumbnail"])
            searched_text = f"""
🔍 __**Informasi Trek Video**__

❇️ **Title:** {x["title"]}
   
⏳ **Duration:** {round(x["duration"] / 60)} Mins
👀 **Views:** `{x["view_count"]}`
👍 **Likes:** `{x["like_count"]}`
👎 **Dislikes:** `{x["dislike_count"]}`
⭐️ **Average Ratings:** {x["average_rating"]}
🎥 **Channel Name:** {x["uploader"]}
📎 **Channel Link:** [Visit From Here]({x["channel_url"]})
🔗 **Link:** [Link]({x["webpage_url"]})

⚡️ __Searched Powered By Steady Music Bot__"""
            link = (x["webpage_url"])
            buttons = personal_markup(link)
            userid = message.from_user.id
            thumb = await down_thumb(thumbnail, userid)
            await app.send_photo(message.chat.id,
                photo=thumb,                 
                caption=searched_text,
                parse_mode="markdown",
                reply_markup=InlineKeyboardMarkup(buttons),
            )
        if str(finxx) == "sud":
            sudoers = await get_sudoers()
            text = "**__Sudo Users List Steady Music:-__**\n\n"
            for count, user_id in enumerate(sudoers, 1):
                try:                     
                    user = await app.get_users(user_id)
                    user = user.first_name if not user.mention else user.mention
                except Exception:
                    continue                     
                text += f"➤ {user}\n"
            if not text:
                await message.reply_text("❌ No Sudo Users")  
            else:
                await message.reply_text(text)

#Join group

@Client.on_message(filters.new_chat_members)
async def new_chat(c: Client, m: Message):
    bot_id = (await c.get_me()).id
    for member in m.new_chat_members:
        if member.id == bot_id:
            return await m.reply(
                "❤️ **Terima kasih telah menambahkan saya ke Grup!**\n\n"
                "**Promosikan saya sebagai admin di Grup, jika tidak saya tidak akan dapat bekerja dengan baik, dan jangan lupa Tekan Tombol Asisstant untuk mengundang asisten.**\n\n"
                "**Selamat Mendengarkan Music❤️",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("📣 Channel", url=f"https://t.me/vtbchannell"),
                            InlineKeyboardButton("💭 Group", url=f"https://t.me/virtualmutualangroup")
                        ],
                        [
                            InlineKeyboardButton("👤 Tambahkan Assistant ke Group 👤", url=f"https://t.me/steadymusicbot?startgroup=true")
                        ]
                    ]
                )
            )
