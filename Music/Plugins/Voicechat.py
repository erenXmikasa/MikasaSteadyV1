import asyncio
import os
import shutil
import subprocess
from sys import version as pyver

from Music.config import get_queue
from pyrogram import Client, filters
from pyrogram.types import Message

from Music import app, db_mem, userbot
from Music.MusicUtilities.database import get_active_chats, is_active_chat


from pyrogram.types import (Message,Voice)

loop = asyncio.get_event_loop()



@app.on_callback_query(filters.regex("timer_checkup_markup"))
async def timer_checkup_markup(_, CallbackQuery):
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    videoid, user_id = callback_request.split("|")
    if await is_active_chat(CallbackQuery.message.chat.id):
        if db_mem[CallbackQuery.message.chat.id]["videoid"] == videoid:
            dur_left = db_mem[CallbackQuery.message.chat.id]["left"]
            duration_min = db_mem[CallbackQuery.message.chat.id]["total"]
            return await CallbackQuery.answer(
                f"Remaining {dur_left} out of {duration_min} Mins.",
                show_alert=True,
            )
        return await CallbackQuery.answer(f"Not Playing.", show_alert=True)
    else:
        return await CallbackQuery.answer(
            f"No Active Voice Chat", show_alert=True
        )


@app.on_message(filters.command("queue"))
async def activevc(_, message: Message):
    global get_queue
    if await is_active_chat(message.chat.id):
        mystic = await message.reply_text("Please Wait... Getting Queue..")
        
        got_queue = get_queue.get(message.chat.id)
        if not got_queue:
            await mystic.edit(f"Nothing in Queue")
        fetched = []
        for get in got_queue:
            fetched.append(get)

        ### Results
        current_playing = fetched[0][0]
        user_name = fetched[0][1]

        msg = "**Queued List**\n\n"
        msg += "**Currently Playing:**"
        msg += "\n▶️" + current_playing[:30]
        msg += f"\n   ╚By:- {user_name}"
        fetched.pop(0)
        if fetched:
            msg += "\n\n"
            msg += "**Up Next In Queue:**"
            for song in fetched:
                name = song[0][:30]
                usr = song[1]
                dur = song[2]
                msg += f"\n⏸️{name}"
                msg += f"\n   ╠Duration : {dur}"
                msg += f"\n   ╚Requested by : {usr}\n"
        if len(msg) > 4096:
            await mystic.delete()
            filename = "queue.txt"
            with open(filename, "w+", encoding="utf8") as out_file:
                out_file.write(str(msg.strip()))
            await message.reply_document(
                document=filename,
                caption=f"**OUTPUT:**\n\n`Queued List`",
                quote=False,
            )
            os.remove(filename)
        else:
            await mystic.edit(msg)
    else:
        await message.reply_text(f"Nothing in Queue")

