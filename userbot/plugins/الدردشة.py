import os
import random

from PIL import Image, ImageDraw, ImageFont
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl.types import InputMessagesFilterDocument, InputMessagesFilterPhotos

from userbot import jmthon

from ..core.managers import edit_or_reply
from ..helpers.utils import reply_id
from . import jmthon, mention

chr = Config.COMMAND_HAND_LER

PICS_STR = []


@jmthon.ar_cmd(pattern="اتمنى ?(.*)")
async def roz(jasem):
    MHD = jasem.pattern_match.group(1)
    success = random.randint(0, 100)
    if MHD:
        reslt = f"""₰ تم ارسال امنيتك \n\n\n️ امنيتك هي: **`{MHD}`** 
              \n\n₰ نسبه نجاحها : **{success}%**"""
    else:
        if jasem.is_reply:
            reslt = f"₰ تم ارسال امنيتك\
                 \n\n₰ نسبه نجاحها : {success}%"
        else:
            reslt = f"₰ تم ارسال امنيتك\
                 \n\n₰ نسبه نجاحها : {success}%"
    await edit_or_reply(jasem, reslt)


@jmthon.ar_cmd(pattern="حالتي$")
async def _(event):
    text = "/start"
    reply_to_id = await reply_id(event)
    await event.edit("**⌔⌔∮ جارِ التحقق انتظر قليلا**")
    chat = "@SpamBot"
    async with event.client.conversation(chat) as conv:
        try:
            await conv.send_message(text)
            message = await conv.get_response(1)
            await event.client.send_message(
                event.chat_id, message, reply_to=reply_to_id
            )
            await event.delete()
        except YouBlockedUserError:
            await event.edit("**⌔∮ يجب عليك الغاء حظر بوت @SpamBot وحاول مره اخرى**")


@jmthon.ar_cmd(pattern="شعار ?(.*)")
async def Logo(event):
    evxnt = await event.edit("**⌔∮ جار التحقق انتظر**")
    text = event.pattern_match.group(1)
    if not text:
        await evxnt.edit("**⪼ يجب عليك كتابه الاسم مع الامر**")
        return
    fnt = await get_font_file(event.client, "@jmthonfonts")
    if event.reply_to_msg_id:
        rply = await event.get_reply_message()
        logo_ = await rply.download_media()
    else:
        async for i in bot.iter_messages(f"@sakkubg", filter=InputMessagesFilterPhotos):
            PICS_STR.append(i)
        pic = random.choice(PICS_STR)
        logo_ = await pic.download_media()
    if len(text) <= 8:
        font_size_ = 100
        strik = 10
    elif len(text) >= 9:
        font_size_ = 50
        strik = 5
    else:
        font_size_ = 120
        strik = 20

    img = Image.open(logo_)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(fnt, font_size_)
    image_widthz, image_heightz = img.size
    w, h = draw.textsize(text, font=font)
    h += int(h * 0.21)
    image_width, image_height = img.size
    draw.text(
        ((image_width - w) / 2, (image_height - h) / 2),
        text,
        font=font,
        fill=(255, 255, 255),
    )
    w_ = (image_width - w) / 2
    h_ = (image_height - h) / 2
    draw.text(
        (w_, h_), text, font=font, fill="white", stroke_width=strik, stroke_fill="black"
    )
    file_name = "Logo.png"
    img.save(
        file_name,
        "png",
    )
    await bot.send_file(
        event.chat_id, file_name, caption=f"⪼ تم صنعه بواسطه : {mention} [@jmthon]"
    )
    await evxnt.delete()
    try:
        os.remove(file_name)
        os.remove(fnt)
        os.remove(logo_)
    except:
        pass


async def get_font_file(client, channel_id):
    font_file_message_s = await client.get_messages(
        entity=channel_id, filter=InputMessagesFilterDocument, limit=None
    )
    font_file_message = random.choice(font_file_message_s)
    return await client.download_media(font_file_message)
