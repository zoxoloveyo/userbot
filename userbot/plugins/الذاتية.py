from userbot import jmthon


@jmthon.ar_cmd(pattern="(جلب الصورة|ذاتية)")
async def roz(bakar):
    if not bakar.is_reply:
        return await bakar.edit(
            "**❃ يجب عليك الرد على صورة ذاتيه التدمير او صورة مؤقته**"
        )
    rr9r7 = await bakar.get_reply_message()
    pic = await rr9r7.download_media()
    await jmthon.send_file("me", pic)
    await bakar.delete()
