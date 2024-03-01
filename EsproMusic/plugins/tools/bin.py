from ... import *
from pyrogram import *
from pyrogram.types import *


@app.on_message(filters.command(["bin", "ccbin", "bininfo"], [".", "!", "/"]))
async def check_ccbin(client, message):
    if len(message.command) < 2:
        return await message.reply_text(
            "<b>Please Give Me a Bin To\nGet Bin Details !</b>"
        )
    try:
        await message.delete()
    except:
        pass
    aux = await message.reply_text("<b>Checking ...</b>")
    bin = message.text.split(None, 1)[1]
    if len(bin) < 6:
        return await aux.edit("<b>❌ Wrong Bin❗...</b>")
    try:
        resp = await api.bininfo(bin)
        await aux.edit(f"""
<b> ✨Vᴀʟɪᴅ Bɪɴ 💯</b>

<b>🏦 Bᴀɴᴋ➪</b> <tt>{resp.bank}</tt>
<b>💳 Bɪɴ➪</b> <tt>{resp.bin}</tt>
<b>🏡 Cᴏᴜɴᴛʀʏ➪</b> <tt>{resp.country}</tt>
<b>🇮🇳 Fʟᴀɢ➪</b> <tt>{resp.flag}</tt>
<b>🧿 Iꜱᴏ➪</b> <tt>{resp.iso}</tt>
<b>⏳ Lᴇᴠᴇʟ➪</b> <tt>{resp.level}</tt>
<b>🔴 Pʀᴇᴘᴀɪᴅ➪</b> <tt>{resp.prepaid}</tt>
<b>🆔 Tʏᴘᴇ➪</b> <tt>{resp.type}</tt>
<b>ℹ️ Vᴇɴᴅᴏʀ➪</b> <tt>{resp.vendor}</tt>"""
        )
    except:
        return await aux.edit(f"""
🚫 BIN not recognized. Please enter a valid BIN.""")
