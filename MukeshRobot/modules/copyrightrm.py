from pyrogram import Client, filters
import os
import logging
from pyrogram.types import *
from pyrogram.errors import FloodWait
from MukeshRobot import pbot as app

# -------------------------------

start_time = time.time()

def time_formatter(milliseconds: float) -> str:
    seconds, milliseconds = divmod(milliseconds, 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return f"{int(hours)}h {int(minutes)}m {int(seconds)}s"

def size_formatter(bytes: int) -> str:
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes < 1024.0:
            break
        bytes /= 1024.0
    return f"{bytes:.2f} {unit}"

def is_protection_enabled():
    setting = settings_collection.find_one({"_id": "global_settings"})
    return setting.get("protection_status", False)



# -----------------------------------------------------------

FORBIDDEN_KEYWORDS = [
    "porn", "xxx", "sex", "NCERT", "XII", "page", "Ans", 
    "meiotic", "divisions", "System.in", "Scanner", 
    "void", "nextInt"
]

@app.on_message(filters.group)
async def handle_message(client, message):
    # Check for text and caption
    if message.text and any(keyword in message.text for keyword in FORBIDDEN_KEYWORDS):
        logging.info(f"✦ Deleting message with ID {message.id}")
        await message.delete()
        user_mention = message.from_user.mention if message.from_user else "User"
        await message.reply_text(f"✦ Hey {user_mention}, please don't send such messages.")
    elif message.caption and any(keyword in message.caption for keyword in FORBIDDEN_KEYWORDS):
        logging.info(f"✦ Deleting message with ID {message.id}")
        await message.delete()
        user_mention = message.from_user.mention if message.from_user else "User"
        await message.reply_text(f"✦ Hey {user_mention}, please avoid sending such content.")

# -----------------------------------------------------------
@app.on_edited_message(filters.group & ~filters.me)
async def delete_edited_messages(client, edited_message):
    await edited_message.delete()

# ------------------------------------------------------------
def delete_long_messages(_, m):
    return m.text and len(m.text.split()) > 400

@app.on_message(filters.group & delete_long_messages)
async def delete_and_reply(client, message):
    await message.delete()
    user_mention = message.from_user.mention if message.from_user else "User"
    await app.send_message(message.chat.id, f"✦ Hey {user_mention}, please keep your messages short.")

# -----------------------------------------------------------
async def delete_pdf_files(client, message):
    if message.document and message.document.mime_type == "application/pdf":
        user_mention = message.from_user.mention if message.from_user else "User"
        warning_message = f"✦ Hey {user_mention}, don't send PDF files due to copyright concerns."
        await message.reply_text(warning_message)
        await message.delete()

@app.on_message(filters.group & filters.document)
async def message_handler(client, message):
    await delete_pdf_files(client, message)
