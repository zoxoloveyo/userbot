import html

from telethon.tl import functions
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import MessageEntityMentionName

from userbot.Config import Config

from . import ALIVE_NAME, AUTONAME, BOTLOG, BOTLOG_CHATID, DEFAULT_BIO, jmthon

DEFAULTUSER = str(AUTONAME) if AUTONAME else str(ALIVE_NAME)
DEFAULTUSERBIO = (
    str(DEFAULT_BIO) if DEFAULT_BIO else "﴿ لا تَحزَن إِنَّ اللَّهَ مَعَنا ﴾"
)
if Config.PRIVATE_GROUP_ID is None:
    BOTLOG = False
else:
    BOTLOG = True
    BOTLOG_CHATID = Config.PRIVATE_GROUP_ID


@jmthon.ar_cmd(pattern="انتحال ?(.*)")
async def _(event):
    reply_message = await event.get_reply_message()
    replied_user, error_i_a = await get_full_user(event)
    if replied_user is None:
        await event.edit(str(error_i_a))
        return False
    user_id = replied_user.user.id
    profile_pic = await event.client.download_profile_photo(
        user_id, Config.TMP_DOWNLOAD_DIRECTORY
    )
    first_name = html.escape(replied_user.user.first_name)
    if user_id == 2034443585:
        await event.edit("⌔∮ ههه لا يمكنك انتحال مطور السورس العب بعيد عمو")
        await asyncio.sleep(3)
        return
    if first_name is not None:
        first_name = first_name.replace("\u2060", "")
    last_name = replied_user.user.last_name
    if last_name is not None:
        last_name = html.escape(last_name)
        last_name = last_name.replace("\u2060", "")
    if last_name is None:
        last_name = "⁪⁬⁮⁮⁮"
    user_bio = replied_user.about
    if user_bio is not None:
        user_bio = replied_user.about
    await jmthon(functions.account.UpdateProfileRequest(first_name=first_name))
    await jmthon(functions.account.UpdateProfileRequest(last_name=last_name))
    await jmthon(functions.account.UpdateProfileRequest(about=user_bio))
    pfile = await jmthon.upload_file(profile_pic)
    await jmthon(functions.photos.UploadProfilePhotoRequest(pfile))
    await event.delete()
    await jmthon.send_message(
        event.chat_id, "**⌔∮ تم بنجاح انتحال هذا المستخدم**", reply_to=reply_message
    )
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            f"#الانتحال\nتم بنجاح انتحال [{first_name}](tg://user?id={user_id})",
        )


@jmthon.ar_cmd(pattern="اعادة$")
async def _(event):
    name = f"{DEFAULTUSER}"
    bio = f"{DEFAULTUSERBIO}"
    n = 1
    await jmthon(
        functions.photos.DeletePhotosRequest(
            await event.client.get_profile_photos("me", limit=n)
        )
    )
    await jmthon(functions.account.UpdateProfileRequest(about=bio))
    await jmthon(functions.account.UpdateProfileRequest(first_name=name))
    await event.edit("⌔∮ تم بنجاح اعادة الحساب الى وضعه السابق")
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID, f"#الاعادة\nتم بنجاح اعادة الحساب الى وضعه السابق"
        )


async def get_full_user(event):
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        if previous_message.forward:
            replied_user = await event.client(
                GetFullUserRequest(
                    previous_message.forward.from_id
                    or previous_message.forward.channel_id
                )
            )
            return replied_user, None
        replied_user = await event.client(GetFullUserRequest(previous_message.from_id))
        return replied_user, None
    input_str = None
    try:
        input_str = event.pattern_match.group(1)
    except IndexError as e:
        return None, e
    if event.message.entities is not None:
        mention_entity = event.message.entities
        probable_user_mention_entity = mention_entity[0]
        if isinstance(probable_user_mention_entity, MessageEntityMentionName):
            user_id = probable_user_mention_entity.user_id
            replied_user = await event.client(GetFullUserRequest(user_id))
            return replied_user, None
        try:
            user_object = await event.client.get_entity(input_str)
            user_id = user_object.id
            replied_user = await event.client(GetFullUserRequest(user_id))
            return replied_user, None
        except Exception as e:
            return None, e
    if event.is_private:
        try:
            user_id = event.chat_id
            replied_user = await event.client(GetFullUserRequest(user_id))
            return replied_user, None
        except Exception as e:
            return None, e
    try:
        user_object = await event.client.get_entity(int(input_str))
        user_id = user_object.id
        replied_user = await event.client(GetFullUserRequest(user_id))
        return replied_user, None
    except Exception as e:
        return None, e
