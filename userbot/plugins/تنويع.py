from asyncio import sleep
from userbot import jmthon
from geopy.geocoders import Nominatim
from telethon.tl import types
from userbot import jmthon
from ..core.managers import edit_or_reply
from ..helpers import reply_id
from covid import Covid
import os
import re
from telethon import Button
from ..Config import Config
from . import jmthon, edit_delete, reply_id

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

@jmthon.ar_cmd(pattern="كورونا(?:\s|$)([\s\S]*)")
async def corona(event):
    input_str = event.pattern_match.group(1)
    country = (input_str).title() if input_str else "world"
    jmthonevent = await edit_or_reply(event, "⪼ يتم سحب المعلومات")
    covid = Covid(source="worldometers")
    try:
        country_data = covid.get_status_by_country_name(country)
    except ValueError:
        country_data = ""
    if country_data:
        hmm1 = country_data["confirmed"] + country_data["new_cases"]
        hmm2 = country_data["deaths"] + country_data["new_deaths"]
        data = ""
        data += f"\n⪼ الاصابات المؤكده : <code>{hmm1}</code>"
        data += f"\n⪼ الاصابات المشبوهه : <code>{country_data['active']}</code>"
        data += f"\n⪼ الوفيات : <code>{hmm2}</code>"
        data += f"\n⪼ الحرجه : <code>{country_data['critical']}</code>"
        data += f"\n⪼ حالات الشفاء : <code>{country_data['recovered']}</code>"
        data += f"\n⪼ اجمالي الاختبارات : <code>{country_data['total_tests']}</code>"
        data += f"\n⪼ الاصابات الجديده : <code>{country_data['new_cases']}</code>"
        data += f"\n⪼ الوفيات الجديده : <code>{country_data['new_deaths']}</code>"
        await jmthonevent.edit(
            "<b>⪼ معلومات كورونا لـ {}:\n{}</b>".format(country, data),
            parse_mode="html",
        )
        else:
            await edit_delete(
                jmthonevent,
                "**⪼ معلومات فايروس كورونا في - {} غير متوفره**".format(country),
                5,
            )
