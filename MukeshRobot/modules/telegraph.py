import os
import requests
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from MukeshRobot import telethn as app
from MukeshRobot.events import register

def upload_file(file_path):
    url = "https://catbox.moe/user/api.php"
    data = {"reqtype": "fileupload", "json": "true"}
    with open(file_path, "rb") as file:
        files = {"fileToUpload": file}
        response = requests.post(url, data=data, files=files)

    if response.status_code == 200:
        try:
            json_response = response.json()
            return True, json_response.get("url", "Unknown URL")
        except Exception:
            return False, "Failed to parse JSON response."
    else:
        return False, f"Error: {response.status_code} - {response.text}"


@register(pattern="^/mtg(m|t) ?(.*)")
async def get_link_group(client, message):
    if not message.reply_to_message:
        return await message.reply_text(
            "❍ Please reply to a media file to upload it to Catbox."
        )

    media = message.reply_to_message
    file_size = 0
    if media.photo:
        file_size = media.photo.file_size
    elif media.video:
        file_size = media.video.file_size
    elif media.document:
        file_size = media.document.file_size

    if file_size > 200 * 1024 * 1024:
        return await message.reply_text("❍ Please provide a media file under 200MB.")

    try:
        text = await message.reply_text("❍ Processing...")

        async def progress(current, total):
            try:
                await text.edit_text(f"❍ Downloading... {current * 100 / total:.1f}%")
            except Exception:
                pass

        local_path = await media.download(progress=progress)
        await text.edit_text("❍ Uploading to Catbox...")

        success, upload_path = upload_file(local_path)

        if success:
            await text.edit_text(
                f"❍ File uploaded successfully!\n[Tap here to view your file]({upload_path})",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                "❍ View File", url=upload_path
                            )
                        ]
                    ]
                ),
                disable_web_page_preview=True,
            )
        else:
            await text.edit_text(
                f"❍ An error occurred while uploading your file.\nReason: {upload_path}"
            )

        try:
            os.remove(local_path)
        except Exception as e:
            print(f"Error while deleting file: {e}")

    except Exception as e:
        await text.edit_text(f"❍ File upload failed.\n\n❍ Reason: {e}")
        return


__help__ = """
 ❍ ɪ ᴄᴀɴ ᴜᴘʟᴏᴀᴅ ғɪʟᴇs ᴛᴏ ᴛᴇʟᴇɢʀᴀᴘʜ


 ❍ /tgm ➛ ɢᴇᴛ ᴛᴇʟᴇɢʀᴀᴘʜ ʟɪɴᴋ ᴏғ ʀᴇᴘʟɪᴇᴅ ᴍᴇᴅɪᴀ
 ❍ /tgt ➛ ɢᴇᴛ ᴛᴇʟᴇɢʀᴀᴘʜ ʟɪɴᴋ ᴏғ ʀᴇᴘʟɪᴇᴅ ᴛᴇxᴛ
 ❍ /tgt [ᴄᴜsᴛᴏᴍ ɴᴀᴍᴇ] ➛ ɢᴇᴛ ᴛᴇʟᴇɢʀᴀᴘʜ ʟɪɴᴋ ᴏғ ʀᴇᴘʟɪᴇᴅ ᴛᴇxᴛ ᴡɪᴛʜ ᴄᴜsᴛᴏᴍ ɴᴀᴍᴇ.
"""

__mod_name__ = "ɢʀᴀᴘʜ"
