import requests
from pyrogram import filters
from pyrogram.types import CallbackQuery, InputMediaPhoto
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from pyrogram.types import Message
from MukeshRobot import pbot as app

close_keyboard = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(text="ʀᴇғʀᴇsʜ", callback_data="refresh_dog"),
            InlineKeyboardButton(text="ᴄʟᴏsᴇ", callback_data="close")
        ],
    ]
)


@app.on_message(filters.command(["dogs", "dog"]))
async def dog(c, m: Message):
    r = requests.get("https://random.dog/woof.json")
    if r.status_code == 200:
        data = r.json()
        dog_url = data["url"]
        if dog_url.endswith(".gif"):
            await m.reply_animation(dog_url, caption="⬤ ᴛʜɪs ɪs ᴅᴏɢ ᴘɪᴄᴛᴜʀᴇ.🐕︎", reply_markup=close_keyboard)
        else:
            await m.reply_photo(dog_url, caption="⬤ ᴛʜɪs ɪs ᴅᴏɢ ᴘɪᴄᴛᴜʀᴇ.🐕︎",  reply_markup=close_keyboard)
    else:
        await m.reply_text("⬤ ғᴀɪʟᴇᴅ ᴛᴏ ғᴇᴛᴄʜ ᴄᴀᴛ ᴘɪᴄᴛᴜʀᴇ. 🐕")


@app.on_callback_query(filters.regex("refresh_dog"))
async def refresh_dog(c, m: CallbackQuery):
    r = requests.get("https://random.dog/woof.json")
    if r.status_code == 200:
        data = r.json()
        dog_url = data["url"]
        if dog_url.endswith(".gif"):
            await m.edit_message_animation(dog_url, caption="⬤ ᴛʜɪs ɪs ᴅᴏɢ ᴘɪᴄᴛᴜʀᴇ. 🐕︎", reply_markup=close_keyboard)
        else:
            await m.edit_message_media(
                InputMediaPhoto(media=dog_url, caption="⬤ ᴛʜɪs ɪs ᴅᴏɢ ᴘɪᴄᴛᴜʀᴇ.🐕︎", ),
                reply_markup=close_keyboard,
            )
    else:
        await m.edit_message_text("⬤ ғᴀɪʟᴇᴅ ᴛᴏ ғᴇᴛᴄʜ ᴄᴀᴛ ᴘɪᴄᴛᴜʀᴇ. 🐕")