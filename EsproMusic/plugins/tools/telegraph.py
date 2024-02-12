from telegraph import upload_file
from pyrogram import filters
import base64
import httpx
import os
from EsproMusic import app
import pyrogram
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from uuid import uuid4
from pyrogram import filters
from pyrogram import Client
from EsproMusic.utils.inline import close_markup

@app.on_message(filters.reply & filters.command(["tgm", "telegraph"]))
async def upscale_image(client, message):
    try:
        if not message.reply_to_message or not message.reply_to_message.photo:
            await message.reply_text("**ᴘʟᴇᴀsᴇ ʀᴇᴘʟʏ ᴛᴏ ᴀɴ ɪᴍᴀɢᴇ ᴛᴏ ᴄʀᴇᴀᴛ ɪᴛs ᴛᴇʟᴇɢʀᴀᴘʜ ʟɪɴᴋ.**")
            return

        sent_message = await message.reply_text("**ᴏᴋ ᴡᴀɪᴛ ᴀ sᴇᴄ ᴍᴀᴋɪɴɢ ᴛᴇʟᴇɢʀᴀᴘʜ ʟɪɴᴋ ᴏғ ʏᴏᴜʀ ɢɪᴠᴇɴ ᴘɪᴄ ᴡɪᴛʜ ғᴜʟʟ ʜᴅ...**")

        image = message.reply_to_message.photo.file_id
        file_path = await client.download_media(image)

        with open(file_path, "rb") as image_file:
            f = image_file.read()

        b = base64.b64encode(f).decode("utf-8")

        async with httpx.AsyncClient() as http_client:
            response = await http_client.post(
                "https://api.qewertyy.me/upscale", data={"image_data": b}, timeout=None
            )

        with open("upscaled_image.png", "wb") as output_file:
            output_file.write(response.content)

        # Upload the upscaled image to Telegraph
        telegraph_url = upload_file("upscaled_image.png")[0]

        # Create caption with the Telegraph link as a button
        button_text = "๏ ᴏᴘᴇɴ ɪɴ ᴛᴇʟᴇɢʀᴀᴘʜ ๏"
        button_url = "https://telegra.ph" + telegraph_url
        reply_markup = InlineKeyboardMarkup(
            [[InlineKeyboardButton(button_text, url=button_url)]]
        )

        await client.send_photo(
            message.chat.id,
            photo="upscaled_image.png",
            caption = f"**➲ ʜᴇʀᴇ ɪs ʏᴏᴜʀ ᴘʜᴏᴛᴏ ᴛᴇʟᴇɢʀᴀᴘʜ ʟɪɴᴋ ɪɴ ʜᴅ.**\n\n**๏ ʏᴏᴜ ᴄᴀɴ ᴄᴏᴘʏ ʙʏ ᴄʟɪᴄᴋ ʜᴇʀᴇ: **\n\n**‣**  `{button_url}`\n\n**๏ ᴍᴀᴋᴇᴅ ʙʏ @{app.username}**",
            reply_markup=reply_markup,
        )

        # Delete the "Wait making link.." message after sending the results
        await sent_message.delete()

    except Exception as e:
        print(f"**ғᴀɪʟᴇᴅ ᴛᴏ ᴜᴘsᴄᴀʟᴇ ᴛʜᴇ ɪᴍᴀɢᴇ**: {e}")
        await message.reply_text("**ғᴀɪʟᴇᴅ ᴛᴏ ᴜᴘsᴄᴀʟᴇ ᴛʜᴇ ɪᴍᴀɢᴇ. ᴘʟᴇᴀsᴇ ᴛʀʏ ᴀɢᴀɪɴ ʟᴀᴛᴇʀ**.")
