from Music import app, OWNER
import os
import subprocess
import shutil
import re
import sys
import traceback
from Music.MusicUtilities.database.sudo import (get_sudoers, get_sudoers, remove_sudo, add_sudo)
from pyrogram import filters, Client
from pyrogram.types import Message

@app.on_message(filters.command("addsudo") & filters.user(OWNER))
async def useradd(_, message: Message):
    if not message.reply_to_message:
        if len(message.command) != 2:
            await message.reply_text("❌ Balas pesan pengguna atau berikan nama pengguna/id_pengguna.")
            return
        user = message.text.split(None, 1)[1]
        if "@" in user:
            user = user.replace("@", "")
        user = (await app.get_users(user))
        from_user = message.from_user 
        sudoers = await get_sudoers()
        if user.id in sudoers:
            return await message.reply_text("✅ Sudah menjadi Pengguna Sudo.")
        added = await add_sudo(user.id)
        if added:
            await message.reply_text(f"✅ Ditambah **{user.mention}** sebagai Sudo")
            return os.execvp("python3", ["python3", "-m", "Music"])
        await edit_or_reply(message, text="❌ Terjadi kesalahan, periksa logs.")  
        return
    from_user_id = message.from_user.id
    user_id = message.reply_to_message.from_user.id
    mention = message.reply_to_message.from_user.mention
    sudoers = await get_sudoers()
    if user_id in sudoers:
        return await message.reply_text("✅ Sudah menjadi Pengguna Sudo.")
    added = await add_sudo(user_id)
    if added:
        await message.reply_text(f"✅ Ditambah **{mention}** sebagai Pengguna Super OwO")
        return os.execvp("python3", ["python3", "-m", "Music"])
    await edit_or_reply(message, text="❌ Terjadi kesalahan, periksa logs.")  
    return    
          
              
@app.on_message(filters.command("delsudo") & filters.user(OWNER))
async def userdel(_, message: Message):
    if not message.reply_to_message:
        if len(message.command) != 2:
            await message.reply_text("❌ Balas pesan pengguna atau berikan nama pengguna/id_pengguna.")
            return
        user = message.text.split(None, 1)[1]
        if "@" in user:
            user = user.replace("@", "")
        user = (await app.get_users(user))
        from_user = message.from_user      
        if user.id not in await get_sudoers():
            return await message.reply_text(f"❌ Bukan bagian dari Steady Sudo.")        
        removed = await remove_sudo(user.id)
        if removed:
            await message.reply_text(f"✅ Dihapus **{user.mention}** dari Sudo.")
            return os.execvp("python3", ["python3", "-m", "Music"])
        await message.reply_text(f"❌ Sesuatu yang salah terjadi.")
        return
    from_user_id = message.from_user.id
    user_id = message.reply_to_message.from_user.id
    mention = message.reply_to_message.from_user.mention
    if user_id not in await get_sudoers():
        return await message.reply_text(f"❌ Bukan bagian dari Steady Sudo.")        
    removed = await remove_sudo(user_id)
    if removed:
        await message.reply_text(f"✅ Dihapus **{mention}** dari Sudo.")
        return os.execvp("python3", ["python3", "-m", "Music"])
    await message.reply_text(f"❌ Sesuatu yang salah terjadi.")
                
                          
@app.on_message(filters.command("sudolist"))
async def sudoers_list(_, message: Message):
    sudoers = await get_sudoers()
    text = "**__Sudo Users List of Steady Music:-__**\n\n"
    for count, user_id in enumerate(sudoers, 1):
        try:                     
            user = await app.get_users(user_id)
            user = user.first_name if not user.mention else user.mention
        except Exception:
            continue                     
        text += f"➤ {user}\n"
    if not text:
        await message.reply_text("❌ Tidak Ada Pengguna Sudo")  
    else:
        await message.reply_text(text) 
