import os
import time
from os import path
import random
import asyncio
import shutil
from pytube import YouTube
from yt_dlp import YoutubeDL
from Music import converter
import yt_dlp
import shutil
import psutil
from pyrogram import Client
from pyrogram.types import Message, Voice
from pytgcalls import StreamType
from pytgcalls.types.input_stream import InputAudioStream, InputStream
from sys import version as pyver
from Music import (
    dbb,
    app,
    BOT_USERNAME,
    BOT_ID,
    BOT_NAME,
    ASSID,
    ASSNAME,
    ASSUSERNAME,
    ASSMENTION,
)
from Music.MusicUtilities.tgcallsrun import (
    music,
    convert,
    download,
    clear,
    get,
    is_empty,
    put,
    task_done,
    ASS_ACC,
)
from Music.MusicUtilities.database.queue import (
    get_active_chats,
    is_active_chat,
    add_active_chat,
    remove_active_chat,
    music_on,
    is_music_playing,
    music_off,
)
from Music.MusicUtilities.database.onoff import (
    is_on_off,
    add_on,
    add_off,
)
from Music.MusicUtilities.database.chats import (
    get_served_chats,
    is_served_chat,
    add_served_chat,
    get_served_chats,
)
from Music.MusicUtilities.helpers.inline import (
    play_keyboard,
    search_markup,
    play_markup,
    playlist_markup,
    audio_markup,
    play_list_keyboard,
)
from Music.MusicUtilities.database.blacklistchat import (
    blacklisted_chats,
    blacklist_chat,
    whitelist_chat,
)
from Music.MusicUtilities.database.gbanned import (
    get_gbans_count,
    is_gbanned_user,
    add_gban_user,
    add_gban_user,
)
from Music.MusicUtilities.database.theme import (
    _get_theme,
    get_theme,
    save_theme,
)
from Music.MusicUtilities.database.assistant import (
    _get_assistant,
    get_assistant,
    save_assistant,
)
from Music.config import DURATION_LIMIT, LOG_GROUP_ID
from Music.MusicUtilities.helpers.decorators import errors
from Music.MusicUtilities.helpers.filters import command
from Music.MusicUtilities.helpers.gets import (
    get_url,
    themes,
    random_assistant,
    ass_det,
)
from Music.MusicUtilities.helpers.logger import LOG_CHAT
from Music.MusicUtilities.helpers.thumbnails import gen_thumb
from Music.MusicUtilities.helpers.chattitle import CHAT_TITLE
from Music.MusicUtilities.helpers.ytdl import ytdl_opts 
from Music.MusicUtilities.helpers.inline import (
    play_keyboard,
    search_markup2,
    search_markup,
)
from pyrogram import filters
from typing import Union
import subprocess
from asyncio import QueueEmpty
import shutil
import os
from youtubesearchpython import VideosSearch
from pyrogram.errors import UserAlreadyParticipant, UserNotParticipant
from pyrogram.types import Message, Audio, Voice
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InputMediaPhoto,
    Message,
)

flex = {}
chat_watcher_group = 3

def time_to_seconds(time):
    stringt = str(time)
    return sum(
        int(x) * 60 ** i for i, x in enumerate(reversed(stringt.split(":")))
    )

@Client.on_message(command("play"))
async def play(_, message: Message):
    chat_id = message.chat.id
 #   if not await is_served_chat(chat_id):
 #       await message.reply_text(f"❌ Not in allowed list chats\n\n{BOT_NAME} is only for allowed chats. Ask any Sudo User to allow your chat.\nCheck Sudo Users List Below",
 #                               reply_markup=InlineKeyboardMarkup(
 #                                   [
 #                                       [
 #                                           InlineKeyboardButton(text="Support Group", url="https://t.me/SteadySupportGroup"),
 #                                           InlineKeyboardButton(text="Channel Update", url="https://t.me/vtbchannell"),
 #                                       ]
 #                                   ]
 #                               ))
 #      return await app.leave_chat(chat_id)  
    if message.sender_chat:
        return await message.reply_text("❌ You're an __Anonymous Admin__!\n✅ Revert back to User Account From Admin Rights.")  
    user_id = message.from_user.id
    chat_title = message.chat.title
    username = message.from_user.first_name
    checking = f"[{message.from_user.first_name}](tg://user?id={message.from_user.id})"
    if await is_on_off(1):
        LOG_ID = LOG_GROUP_ID
        if int(chat_id) != int(LOG_ID):
            return await message.reply_text(f">> ❌ Bot is under Maintenance, Sorry for the inconvenience!")
        return await message.reply_text(f">> ❌ Bot is under Maintenance, Sorry for the inconvenience!")
    a = await app.get_chat_member(message.chat.id , BOT_ID)
    if a.status != "administrator":
        await message.reply_text(f"I need to be admin with some permissions:\n\n>> **can_manage_voice_chats:** To manage voice chats\n>> **can_delete_messages:** To delete Music's Searched Waste\n>> **can_invite_users**: For inviting assistant to chat\n>> **can_restrict_members**: For Protecting Music from Spammers.")
        return
    if not a.can_manage_voice_chats:
        await message.reply_text(
        "❌ I don't have the required permission to perform this action."
        + "\n**Permission:** __MANAGE VOICE CHATS__")
        return
    if not a.can_delete_messages:
        await message.reply_text(
        "❌ I don't have the required permission to perform this action."
        + "\n**Permission:** __DELETE MESSAGES__")
        return
    if not a.can_invite_users:
        await message.reply_text(
        "❌ I don't have the required permission to perform this action."
        + "\n**Permission:** __INVITE USERS VIA LINK__")
        return
    if not a.can_restrict_members:
        await message.reply_text(
        "❌ I don't have the required permission to perform this action."
        + "\n**Permission:** __BAN USERS__")
        return
    try:
        b = await app.get_chat_member(message.chat.id , ASSID) 
        if b.status == "kicked":
            await message.reply_text(f"❌ {ASSNAME}(@{ASSUSERNAME}) is banned in your chat **{chat_title}**\n\nUnban it first to use Music")
            return
    except UserNotParticipant:
        if message.chat.username:
            try: 
                await ASS_ACC.join_chat(f"{message.chat.username}")
                await message.reply(f"✅ {ASSNAME} Joined Successfully",) 
                await remove_active_chat(chat_id)
            except Exception as e:
                await message.reply_text(f"❌ __**Assistant Failed To Join**__\n\n**Reason**:{e}")
                return
        else:
            try:
                xxy = await app.export_chat_invite_link(message.chat.id)
                yxy = await app.revoke_chat_invite_link(message.chat.id, xxy)
                await ASS_ACC.join_chat(yxy.invite_link)
                await message.reply(f"✅ {ASSNAME} Joined Successfully",) 
                await remove_active_chat(chat_id)
            except UserAlreadyParticipant:
                pass
            except Exception as e:
                return await message.reply_text(f"❌ __**Assistant Failed To Join**__\n\n**Reason**:{e}")       
    audio = (message.reply_to_message.audio or message.reply_to_message.voice) if message.reply_to_message else None
    url = get_url(message)
    await message.delete()
    fucksemx = 0
    if audio:
        fucksemx = 1
        what = "Audio Searched"
        await LOG_CHAT(message, what)
        mystic = await message.reply_text(f"**🔄 Processing Audio Given By {username}**")
        if audio.file_size > 157286400:
            await mystic.edit_text("❌ Audio File Size Should Be Less Than 150 mb") 
            return
        duration = round(audio.duration / 60)
        if duration > DURATION_LIMIT:
            return await mystic.edit_text(f"❌ **__Duration Error__**\n\n**Allowed Duration: **{DURATION_LIMIT} minute(s)\n**Received Duration:** {duration} minute(s)")
        file_name = audio.file_unique_id + '.' + (
            (
                audio.file_name.split('.')[-1]
            ) if (
                not isinstance(audio, Voice)
            ) else 'ogg'
        )
        file_name = path.join(path.realpath('
