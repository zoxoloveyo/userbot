from asyncio import sleep

from geopy.geocoders import Nominatim
from telethon import Button
from telethon.tl import types

from ..core.managers import edit_or_reply
from ..helpers import reply_id
from . import edit_delete, jmthon, reply_id


@jmthon.ar_cmd(pattern="لستة(?: |$)(.*)")
async def _(event):
    reply_to_id = await reply_id(event)
    reply_message = await event.get_reply_message()
    if reply_message:
        markdown_note = reply_message.text
    else:
        markdown_note = "".join(event.text.split(maxsplit=1)[1:])
    if not markdown_note:
        return await edit_delete(event, "₰ يجب عليك وضع مسافـة لاستخدامها مع الامر ")
    await make_inline(markdown_note, event.client, event.chat_id, reply_to_id)
    await event.delete()


def build_keyboard(buttons):
    keyb = []
    for btn in buttons:
        if btn[2] and keyb:
            keyb[-1].append(Button.url(btn[0], btn[1]))
        else:
            keyb.append([Button.url(btn[0], btn[1])])
    return keyb


@jmthon.ar_cmd(pattern="موقع ([\s\S]*)")
async def gps(event):
    reply_to_id = await reply_id(event)
    input_str = event.pattern_match.group(1)
    catevent = await edit_or_reply(event, "⪼ يتم العثور على الموقع المطلوب")
    geolocator = Nominatim(user_agent="jmthon")
    geoloc = geolocator.geocode(input_str)
    if geoloc:
        lon = geoloc.longitude
        lat = geoloc.latitude
        await event.client.send_file(
            event.chat_id,
            file=types.InputMediaGeoPoint(types.InputGeoPoint(lat, lon)),
            caption=f"**الموقع : **{input_str}",
            reply_to=reply_to_id,
        )
        await catevent.delete()
    else:
        await catevent.edit("⪼ لم أجد الموقع 𓆰")


@jmthon.ar_cmd(pattern="مؤقتا (\d*) ([\s\S]*)")
async def _(event):
    jmthon = ("".join(event.text.split(maxsplit=1)[1:])).split(" ", 1)
    message = jmthon[1]
    ttl = int(jmthon[0])
    await event.delete()
    await sleep(ttl)
    await event.respond(message)
