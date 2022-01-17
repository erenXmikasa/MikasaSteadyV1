import asyncio
import os
from Music.MusicUtilities.tgcallsrun import ASS_ACC

from pyrogram import Client, filters
from pyrogram.errors import UserAlreadyParticipant, UserNotParticipant
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from pytgcalls import StreamType
from pytgcalls.types.input_stream import AudioVideoPiped
from pytgcalls.types.input_stream.quality import (
    HighQualityAudio,
    HighQualityVideo,
    LowQualityVideo,
    MediumQualityVideo,
)
from youtubesearchpython import VideosSearch
from Music.config import GROUP, CHANNEL
from Music import BOT_NAME, BOT_USERNAME, app
from Music.MusicUtilities.tgcallsrun.music import pytgcalls as call_py
from Music.MusicUtilities.helpers.filters import command
from Music.MusicUtilities.helpers.logger import LOG_CHAT
from Music.MusicUtilities.tgcallsrun.queues import (
    QUEUE,
    add_to_queue,
    clear_queue,
    get_queue,
)
from Music.MusicUtilities.helpers.inline import (
    play_keyboard,
    search_markup,
    search_markup2,
    play_markup,
    playlist_markup,
    audio_markup,
    play_list_keyboard,
)


def ytsearch(query):
    try:
        search = VideosSearch(query, limit=5).result()
        data = search["result"][0]
        songname = data["title"]
        url = data["link"]
        duration = data["duration"]
        thumbnail = f"https://i.ytimg.com/vi/{data['id']}/hqdefault.jpg"
        return [songname, url, duration, thumbnail]
    except Exception as e:
        print(e)
        return 0


async def ytdl(link):
    proc = await asyncio.create_subprocess_exec(
        "yt-dlp",
        "-g",
        "-f",
        "best[height<=?720][width<=?1280]",
        f"{link}",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await proc.communicate()
    if stdout:
        return 1, stdout.decode().split("\n")[0]
    else:
        return 0, stderr.decode()



@app.on_message(command("videoplay") & filters.group)
async def vplay(c: Client, message: Message):
    replied = message.reply_to_message
    chat_id = message.chat.id
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    rpk = "[" + user_name + "](tg://user?id=" + str(user_id) + ")"

    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text="▶️", callback_data=f'cbresume'),
                InlineKeyboardButton(text="⏸️", callback_data=f'cbpause'),
                InlineKeyboardButton(text="⏭️", callback_data=f'skipvc'),
                InlineKeyboardButton(text="⏹️", callback_data=f'cbstop')
            ],
            [
                InlineKeyboardButton(text="Tutup", callback_data="close")
            ],
        ]
    )

    if message.sender_chat:
        return await message.reply_text(
            "Anda adalah **Admin Anonim!**\n\n» kembali ke akun pengguna dari hak admin."
        )
    try:
        aing = await c.get_me()
    except Exception as e:
        return await message.reply_text(f"error:\n\n{e}")
    a = await c.get_chat_member(chat_id, aing.id)
    if a.status != "administrator":
        await message.reply_text(
            f"""
💡 Untuk menggunakan saya, Saya perlu menjadi admin dengan izin:
» ❌ Hapus pesan
» ❌ Blokir pengguna
» ❌ Tambah pengguna
» ❌ Kelola obrolan suara
✨ Powered by: [{BOT_NAME}](t.me/{BOT_USERNAME})
""",
            disable_web_page_preview=True,
        )
        return
    if not a.can_manage_voice_chats:
        await message.reply_text(
            f"""
💡 Untuk menggunakan saya, Saya perlu menjadi admin dengan izin:
» ❌ Kelola obrolan suara
✨ Powered by: [{BOT_NAME}](t.me/{BOT_USERNAME})
""",
            disable_web_page_preview=True,
        )
        return
    if not a.can_delete_messages:
        await message.reply_text(
            f"""
💡 Untuk menggunakan saya, Saya perlu menjadi admin dengan izin:
» ❌ Hapus pesan
✨ Powered by: [{BOT_NAME}](t.me/{BOT_USERNAME})
""",
            disable_web_page_preview=True,
        )
        return
    if not a.can_invite_users:
        await message.reply_text(
            f"""
💡 Untuk menggunakan saya, Saya perlu menjadi admin dengan izin:
» ❌ Tambah pengguna
✨ Powered by: [{BOT_NAME}](t.me/{BOT_USERNAME})
""",
            disable_web_page_preview=True,
        )
        return
    try:
        ubot = await ASS_ACC.get_me()
        b = await c.get_chat_member(chat_id, ubot.id)
        if b.status == "kicked":
            await message.reply_text(
                f"@{ubot.username} **Terkena ban di grup** {message.chat.title}\n\n» **unban Assistant terlebih dahulu jika ingin menggunakan bot ini.**"
            )
            return
    except UserNotParticipant:
        if message.chat.username:
            try:
                await ASS_ACC.join_chat(message.chat.username)
            except Exception as e:
                await message.reply_text(
                    f"❌ **@{ubot.username} Assistant gagal bergabung**\n\n**Alasan**: `{e}`"
                )
                return
        else:
            try:
                invite_link = await message.chat.export_invite_link()
                if "+" in invite_link:
                    link_hash = (invite_link.replace("+", "")).split("t.me/")[1]
                await ASS_ACC.join_chat(f"https://t.me/joinchat/{link_hash}")
            except UserAlreadyParticipant:
                pass
            except Exception as e:
                return await message.reply_text(
                    f"❌ **@{ubot.username} Assistant gagal bergabung**\n\n**Alasan**: `{e}`"
                )
            return
        what = "Query Given"
        await LOG_CHAT(message, what)
        query = message.text.split(None, 1)[1]
        mystic = await message.reply_text("**🔎 Pencarian**")
        try:
            a = VideosSearch(query, limit=5)
            result = (a.result()).get("result")
            title1 = result[0]["title"]
            duration1 = result[0]["duration"]
            title2 = result[1]["title"]
            duration2 = result[1]["duration"]
            title3 = result[2]["title"]
            duration3 = result[2]["duration"]
            title4 = result[3]["title"]
            duration4 = result[3]["duration"]
            title5 = result[4]["title"]
            duration5 = result[4]["duration"]
            ID1 = result[0]["id"]
            ID2 = result[1]["id"]
            ID3 = result[2]["id"]
            ID4 = result[3]["id"]
            ID5 = result[4]["id"]
        except Exception as e:
            return await mystic.edit_text(
                f"Lagu Tidak Ditemukan.\n**Kemungkinan Alasan:** {e}"
            )
        thumb ="cache/IMG_20211203_150634_304.jpg"
        buttons = search_markup(ID1, ID2, ID3, ID4, ID5, duration1, duration2, duration3, duration4, duration5, user_id, query)
        await mystic.edit( 
            f"**✨ Silahkan pilih lagu yang ingin anda putar**\n\n¹ <b>{title1[:27]}</b>\n  ┗ 💡 <u>__[More Information](https://t.me/{BOT_USERNAME}?start=info_{ID1})__</u>\n  ┗ ⚡ __Powered by {BOT_NAME}__\n\n² <b>{title2[:27]}</b>\n  ┗ 💡 <u>__[More Information](https://t.me/{BOT_USERNAME}?start=info_{ID2})__</u>\n  ┗ ⚡ __Powered by {BOT_NAME}__\n\n³ <b>{title3[:27]}</b>\n  ┗ 💡 <u>__[More Information](https://t.me/{BOT_USERNAME}?start=info_{ID3})__</u>\n  ┗ ⚡ __Powered by {BOT_NAME}__\n\n⁴ <b>{title4[:27]}</b>\n  ┗ 💡 <u>__[More Information](https://t.me/{BOT_USERNAME}?start=info_{ID4})__</u>\n  ┗ ⚡ __Powered by {BOT_NAME}__\n\n⁵ <b>{title5[:27]}</b>\n  ┗ 💡 <u>__[More Information](https://t.me/{BOT_USERNAME}?start=info_{ID5})__</u>\n  ┗ ⚡ __Powered by {BOT_NAME}__",    
            reply_markup=InlineKeyboardMarkup(buttons),
            disable_web_page_preview=True
                   )
    if replied:
        if replied.video or replied.document:
            what = "Audio Searched"
            await LOG_CHAT(message, what)
            loser = await replied.reply("📥 **Mengunduh Video...**")
            dl = await replied.download()
            link = replied.link
            if len(message.command) < 2:
                Q = 720
            else:
                pq = message.text.split(None, 1)[1]
                if pq == "720" or "480" or "360":
                    Q = int(pq)
                else:
                    Q = 720
                    await loser.edit(
                        "» **Hanya 720, 480, 360 yang diizinkan** \n💡 **Sekarang Streaming Video Dalam 720p**"
                    )
            try:
                if replied.video:
                    songname = replied.video.file_name[:70]
                elif replied.document:
                    songname = replied.document.file_name[:70]
            except BaseException:
                songname = "Video"

            if chat_id in QUEUE:
                pos = add_to_queue(chat_id, songname, dl, link, "Video", Q)
                await loser.delete()
                requester = f"[{message.from_user.first_name}](tg://user?id={message.from_user.id})"
                await app.send_message(
                    chat_id,
                    f"""
💡 **Trek ditambahkan ke antrian**
🏷 **Nama:** [{songname[:999]}]({link})
🎧 **Atas permintaan:** {requester}
#️⃣ **Posisi antrian** {pos}
""",
                    disable_web_page_preview=True,
                    reply_markup=keyboard,
                )
            else:
                if Q == 720:
                    amaze = HighQualityVideo()
                elif Q == 480:
                    amaze = MediumQualityVideo()
                elif Q == 360:
                    amaze = LowQualityVideo()
                await call_py.join_group_call(
                    chat_id,
                    AudioVideoPiped(
                        dl,
                        HighQualityAudio(),
                        amaze,
                    ),
                    stream_type=StreamType().pulse_stream,
                )
                add_to_queue(chat_id, songname, dl, link, "Video", Q)
                await loser.delete()
                requester = f"[{message.from_user.first_name}](tg://user?id={message.from_user.id})"
                await app.send_message(
                    chat_id,
                    f"""
▶️ **Streaming video dimulai**
🏷 **Nama:** [{songname[:999]}]({link})
🎧 **Atas permintaan:** {requester}
💬 **Diputar di:** {message.chat.title}
""",
                    disable_web_page_preview=True,
                    reply_markup=keyboard,
                )

    else:
        if len(message.command) < 2:
            await message.reply(
                "» Balas ke **file video** atau **berikan sesuatu untuk ditelusuri.**"
            )
        else:
            what = "Query Given"
            await LOG_CHAT(message, what)
            loser = await message.reply("🔎 **Pencarian**")
            query = message.text.split(None, 1)[1]
            search = ytsearch(query)
        try:
            a = VideosSearch(query, limit=5)
            result = (a.result()).get("result")
            title1 = result[0]["title"]
            duration1 = result[0]["duration"]
            title2 = result[1]["title"]
            duration2 = result[1]["duration"]
            title3 = result[2]["title"]
            duration3 = result[2]["duration"]
            title4 = result[3]["title"]
            duration4 = result[3]["duration"]
            title5 = result[4]["title"]
            duration5 = result[4]["duration"]
            ID1 = result[0]["id"]
            ID2 = result[1]["id"]
            ID3 = result[2]["id"]
            ID4 = result[3]["id"]
            ID5 = result[4]["id"]
        except Exception as e:
            return await mystic.edit_text(
                f"Lagu Tidak Ditemukan.\n**Kemungkinan Alasan:** {e}"
            Q = 480
            amaze = HighQualityVideo()
            if search == 0:
                await loser.edit("❌ **Tidak ada hasil yang ditemukan.**")
            else:
                songname = search[0]
                url = search[1]
                duration = search[2]
                thumbnail = search[3]
                veez, ytlink = await ytdl(url)
                if veez == 0:
                    await loser.edit(f"❌ yt-dl masalah terdeteksi\n\n» `{ytlink}`")
                else:
                    if chat_id in QUEUE:
                        pos = add_to_queue(chat_id, songname, ytlink, url, "Video", Q)
                        await loser.delete()
                        requester = f"[{message.from_user.first_name}](tg://user?id={message.from_user.id})"
                        await app.send_message(
                                chat_id,
                                f"""
💡 **Trek ditambahkan ke antrian**
🏷 **Nama:** [{songname[:999]}]({url})
⏱️ **Durasi:** {duration}
🎧 **Atas permintaan:** {requester}
#️⃣ **Posisi antrian** {pos}
""",
                            disable_web_page_preview=True,
                            reply_markup=keyboard,
                        )
                    else:
                        try:
                            await call_py.join_group_call(
                                chat_id,
                                AudioVideoPiped(
                                    ytlink,
                                    HighQualityAudio(),
                                    amaze,
                                ),
                                stream_type=StreamType().pulse_stream,
                            )
                            add_to_queue(chat_id, songname, ytlink, url, "Video", Q)
                            await loser.delete()
                            requester = f"[{message.from_user.first_name}](tg://user?id={message.from_user.id})"
                            await app.send_message(
                                chat_id,
                                f"""
▷ **Memutar video dimulai**
🏷 **Nama:** [{songname[:999]}]({url})
⏱️ **Durasi:** {duration}
🎧 **Atas permintaan:** {requester}
💬 **Diputar di:** {message.chat.title}
""",
                                disable_web_page_preview=True,
                                reply_markup=keyboard,
                            )
                        except Exception as ep:
                            await loser.delete()
                            await message.reply_text(f"Error: `{ep}`")


@Client.on_callback_query(filters.regex(pattern=r"popat"))
async def popat(_,CallbackQuery): 
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    print(callback_request)
    userid = CallbackQuery.from_user.id 
    try:
        id , query, user_id = callback_request.split("|") 
    except Exception as e:
        return await CallbackQuery.message.edit(f"❌ Error Occured\n**Possible reason could be**:{e}")       
    if CallbackQuery.from_user.id != int(user_id):
        return await CallbackQuery.answer("❌ This is not for you! Search You Own Song", show_alert=True)
    i=int(id)
    query = str(query)
    try:
        a = VideosSearch(query, limit=10)
        result = (a.result()).get("result")
        title1 = (result[0]["title"])
        duration1 = (result[0]["duration"])
        title2 = (result[1]["title"])
        duration2 = (result[1]["duration"])      
        title3 = (result[2]["title"])
        duration3 = (result[2]["duration"])
        title4 = (result[3]["title"])
        duration4 = (result[3]["duration"])
        title5 = (result[4]["title"])
        duration5 = (result[4]["duration"])
        title6 = (result[5]["title"])
        duration6 = (result[5]["duration"])
        title7= (result[6]["title"])
        duration7 = (result[6]["duration"])      
        title8 = (result[7]["title"])
        duration8 = (result[7]["duration"])
        title9 = (result[8]["title"])
        duration9 = (result[8]["duration"])
        title10 = (result[9]["title"])
        duration10 = (result[9]["duration"])
        ID1 = (result[0]["id"])
        ID2 = (result[1]["id"])
        ID3 = (result[2]["id"])
        ID4 = (result[3]["id"])
        ID5 = (result[4]["id"])
        ID6 = (result[5]["id"])
        ID7 = (result[6]["id"])
        ID8 = (result[7]["id"])
        ID9 = (result[8]["id"])
        ID10 = (result[9]["id"])                    
    except Exception as e:
        return await mystic.edit_text(f"❌ Soung Not Found.\n**Possible Reason:**{e}")
    if i == 1:
        buttons = search_markup2(ID6, ID7, ID8, ID9, ID10, duration6, duration7, duration8, duration9, duration10 ,user_id, query)
        await CallbackQuery.edit_message_text(
            f"6️⃣ <b>{title6}</b>\n  ┗  💡 <u>__[More Information](https://t.me/vckyclone)__</u>\n\n7️⃣ <b>{title7}</b>\n  ┗  💡 <u>__[More Information](https://t.me/vckyclone)__</u>\n\n8️⃣ <b>{title8}</b>\n  ┗  💡 <u>__[More Information](https://t.me/vckyclone)__</u>\n\n9️⃣ <b>{title9}</b>\n  ┗  💡 <u>__[More Information](https://t.me/vckyclone)__</u>\n\n🔟 <b>{title10}</b>\n  ┗  💡 <u>__[More Information](https://t.me/vckyclone)__</u>\n Powered by 𝙎𝙩𝙚𝙖𝙙𝙮 𝙈𝙪𝙨𝙞𝙘 𝘽𝙤𝙩",    
            reply_markup=InlineKeyboardMarkup(buttons),
            disable_web_page_preview=True
        )  
        return    
    if i == 2:
        buttons = search_markup(ID1, ID2, ID3, ID4, ID5, duration1, duration2, duration3, duration4, duration5, user_id, query)
        await CallbackQuery.edit_message_text(
            f"1️⃣ <b>{title1}</b>\n  ┗  💡 <u>__[More Information](https://t.me/vckyclone)__</u>\n\n2️⃣ <b>{title2}</b>\n  ┗  💡 <u>__[More Information](https://t.me/vckyclone)__</u>\n\n3️⃣ <b>{title3}</b>\n  ┗  💡 <u>__[More Information](https://t.me/vckyclone)__</u>\n\n4️⃣ <b>{title4}</b>\n  ┗  💡 <u>__[More Information](https://t.me/vckyclone)__</u>\n\n5️⃣ <b>{title5}</b>\n  ┗  💡 <u>__[More Information](https://t.me/vckyclone)__</u>",    
            reply_markup=InlineKeyboardMarkup(buttons),
            disable_web_page_preview=True 
        )  
        return


@app.on_message(command("videoplaylist") & filters.group)
async def playlist(client, m: Message):
    chat_id = m.chat.id
    if chat_id in QUEUE:
        chat_queue = get_queue(chat_id)
        if len(chat_queue) == 1:
            await m.delete()
            await m.reply(
                f"**🎧 SEKARANG MEMUTAR:** \n[{chat_queue[0][0]}]({chat_queue[0][2]}) | `{chat_queue[0][3]}`",
                disable_web_page_preview=True,
            )
        else:
            QUE = f"**🎧 SEKARANG MEMUTAR:** \n[{chat_queue[0][0]}]({chat_queue[0][2]}) | `{chat_queue[0][3]}` \n\n**⏯ DAFTAR ANTRIAN:**"
            l = len(chat_queue)
            for x in range(1, l):
                hmm = chat_queue[x][0]
                hmmm = chat_queue[x][2]
                hmmmm = chat_queue[x][3]
                QUE = QUE + "\n" + f"**#{x}** - [{hmm}]({hmmm}) | `{hmmmm}`\n"
            await m.reply(QUE, disable_web_page_preview=True)
    else:
        await m.reply("**❌ Tidak memutar apapun**")

