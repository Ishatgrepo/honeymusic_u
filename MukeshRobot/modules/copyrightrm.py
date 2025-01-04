from pyrogram import Client, filters
import os
import logging
from pyrogram.types import *
from pyrogram.errors import FloodWait
from MukeshRobot import pbot as app
import unicodedata
from ftfy import fix_text
from unidecode import unidecode
import psutil
import time
import platform

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

def normalize_text(text):
    if not text:
        return ""
    try:
        # Normalize to NFKC form (decompose characters like "é" to "e" + "´")
        text = unicodedata.normalize("NFKC", text)
        
        # Fix any corrupted Unicode text using ftfy
        text = fix_text(text)
        
        # Use unidecode to remove non-ASCII characters and replace them with nearest ASCII equivalent
        text = unidecode(text)
        
        # Final cleanup to remove any non-printable or unwanted characters
        text = ''.join(c for c in text if unicodedata.category(c) != 'Cc')
        
        return text
    except UnicodeDecodeError as e:
        logging.error(f"UnicodeDecodeError encountered while normalizing text: {e}")
        try:
            # Attempt to decode using utf-8 and ignore errors
            text = text.encode('utf-8', 'ignore').decode('utf-8', 'ignore')
            return text
        except Exception as inner_e:
            logging.error(f"Error while attempting to handle broken encoding: {inner_e}")
            return text  # Return text as-is if error persists
    except Exception as e:
        logging.error(f"Error encountered while normalizing text: {e}")
        return text  # Return text as-is if any other error occurs

@app.on_message(filters.command("protect"))
async def protect_command_handler(_, message: Message):
    command = message.text.strip().lower()
    
    if command == "/protect on":
        settings_collection.update_one(
            {"_id": "global_settings"},
            {"$set": {"protection_status": True}}
        )
        await message.reply_text("🔒 **Pʀᴏᴛᴇᴄᴛɪᴏɴ Eɴᴀʙʟᴇᴅ**!.")
    
    elif command == "/protect off":
        settings_collection.update_one(
            {"_id": "global_settings"},
            {"$set": {"protection_status": False}}
        )
        await message.reply_text("🔓 **Pʀᴏᴛᴇᴄᴛɪᴏɴ Dɪsᴀʙʟᴇᴅ**!.")
    
    else:
        await message.reply_text("**➥ Usᴇ ᴄᴏʀʀᴇᴄᴛ ᴏɴ ⤒ ᴏғғ**\n\n⇝ `/protect on` - ᴇɴᴀʙʟᴇ\n⇝ `/protect off` - ᴅɪsᴀʙʟᴇ")


# Handle Forbidden Keywords

@app.on_message()
async def handle_message(client, message: Message):
    if is_protection_enabled():
        # Normalize message text and caption
        text = normalize_text(message.text) if message.text else ""
        caption = normalize_text(message.caption) if message.caption else ""

        # Check if any forbidden keyword is in the normalized text or caption
        if any(keyword in text.lower() for keyword in FORBIDDEN_KEYWORDS):
            logging.info(f"Deleting message with ID {message.id} due to forbidden keyword in text")
            await message.delete()
            await message.reply_text(
                f"@{message.from_user.username} Dᴏɴ'ᴛ sᴇɴᴅ ɴᴇxᴛ ᴛɪᴍᴇ ᴏᴛʜᴇʀᴡɪsᴇ ʙᴀɴɴᴇᴅ ʙʏ ᴀᴅᴍɪɴ !"
            )
        elif any(keyword in caption.lower() for keyword in FORBIDDEN_KEYWORDS):
            logging.info(f"Deleting message with ID {message.id} due to forbidden keyword in caption")
            await message.delete()
            await message.reply_text(
                f"@{message.from_user.username} Dᴏɴ'ᴛ sᴇɴᴅ ɴᴇxᴛ ᴛɪᴍᴇ ᴏᴛʜᴇʀᴡɪsᴇ ʙᴀɴɴᴇᴅ ʙʏ ᴀᴅᴍɪɴ !"
            )

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
