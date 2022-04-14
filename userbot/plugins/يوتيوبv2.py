import asyncio
import glob
import io
import os
import pathlib
from time import time

from telethon.tl import types
from telethon.utils import get_attributes
from urlextract import URLExtract
from wget import download
from yt_dlp import YoutubeDL
from yt_dlp.utils import (
    ContentTooShortError,
    DownloadError,
    ExtractorError,
    GeoRestrictedError,
    MaxDownloadsReached,
    PostProcessingError,
    UnavailableVideoError,
    XAttrMetadataError,
)

from ..core import pool
from ..core.logger import logging
from ..core.managers import edit_delete, edit_or_reply
from ..helpers import progress, reply_id
from ..helpers.functions.utube import _mp3Dl, get_yt_video_id, get_ytthumb, ytsearch
from ..helpers.utils import _format

BASE_YT_URL = "https://www.youtube.com/watch?v="
extractor = URLExtract()
LOGS = logging.getLogger(__name__)

plugin_category = "تحميل"


video_opts = {
    "format": "best",
    "addmetadata": True,
    "key": "FFmpegMetadata",
    "writethumbnail": True,
    "prefer_ffmpeg": True,
    "geo_bypass": True,
    "nocheckcertificate": True,
    "postprocessors": [
        {"key": "FFmpegVideoConvertor", "preferedformat": "mp4"},
        {"key": "FFmpegMetadata"},
    ],
    "outtmpl": "cat_ytv.mp4",
    "logtostderr": False,
    "quiet": True,
}


async def ytdl_down(event, opts, url):
    ytdl_data = None
    try:
        await event.edit("**- يتم الفحص عن البيانات انتظر قليلا**")
        with YoutubeDL(opts) as ytdl:
            ytdl_data = ytdl.extract_info(url)
    except DownloadError as DE:
        await event.edit(f"`{DE}`")
    except ContentTooShortError:
        await event.edit("- عذرا يبدو ان محتوى التنزيل قصير جدا  .")
    except GeoRestrictedError:
        await event.edit(
            "** - الفيديو غير متاح من موقعك الجغرافي بسبب القيود الجغرافية التي يفرضها موقع الويب**"
        )
    except MaxDownloadsReached:
        await event.edit("-  تم الوصول إلى الحد الأقصى لعدد التنزيلات")
    except PostProcessingError:
        await event.edit("- لقد حدث خطأ اثتاء المعالجه")
    except UnavailableVideoError:
        await event.edit("- هذه الصيغه غير متوفره حسب طلبك")
    except XAttrMetadataError as XAME:
        await event.edit(f"`{XAME.code}: {XAME.msg}\n{XAME.reason}`")
    except ExtractorError:
        await event.edit("- لقد حدث خطأ اثناء التعرف على المعلومات")
    except Exception as e:
        await event.edit(f"**خطأ : **\n__{e}__")
    return ytdl_data


async def fix_attributes(
    path, info_dict: dict, supports_streaming: bool = False, round_message: bool = False
) -> list:
    """Avoid multiple instances of an attribute."""
    new_attributes = []
    video = False
    audio = False

    uploader = info_dict.get("uploader", "Unknown artist")
    duration = int(info_dict.get("duration", 0))
    suffix = path.suffix[1:]
    if supports_streaming and suffix != "mp4":
        supports_streaming = True

    attributes, mime_type = get_attributes(path)
    if suffix == "صوتي":
        title = str(info_dict.get("title", info_dict.get("id", "Unknown title")))
        audio = types.DocumentAttributeAudio(
            duration=duration, voice=None, title=title, performer=uploader
        )
    elif suffix == "فيديو":
        width = int(info_dict.get("width", 0))
        height = int(info_dict.get("height", 0))
        for attr in attributes:
            if isinstance(attr, types.DocumentAttributeVideo):
                duration = duration or attr.duration
                width = width or attr.w
                height = height or attr.h
                break
        video = types.DocumentAttributeVideo(
            duration=duration,
            w=width,
            h=height,
            round_message=round_message,
            supports_streaming=supports_streaming,
        )

    if audio and isinstance(audio, types.DocumentAttributeAudio):
        new_attributes.append(audio)
    if video and isinstance(video, types.DocumentAttributeVideo):
        new_attributes.append(video)

    new_attributes.extend(
        attr
        for attr in attributes
        if (
            isinstance(attr, types.DocumentAttributeAudio)
            and not audio
            or not isinstance(attr, types.DocumentAttributeAudio)
            and not video
            or not isinstance(attr, types.DocumentAttributeAudio)
            and not isinstance(attr, types.DocumentAttributeVideo)
        )
    )
    return new_attributes, mime_type


@jmthon.ar_cmd(
    pattern="تحميل(صوتي)(?:\s|$)([\s\S]*)",
    command=("تحميل", plugin_category),
)
async def download_audio(event):
    """To download audio from YouTube and many other sites."""
    msg = event.pattern_match.group(1)
    rmsg = await event.get_reply_message()
    if not msg and rmsg:
        msg = rmsg.text
    urls = extractor.find_urls(msg)
    if not urls:
        return await edit_or_reply(
            event, "**⌯︙ يرجى الرد على الرسالة او كتابة الرابط اولا**"
        )
    catevent = await edit_or_reply(event, "⌯︙يتم البحث عن المطلوب انتظر")
    reply_to_id = await reply_id(event)
    for url in urls:
        try:
            vid_data = YoutubeDL({"no-playlist": True}).extract_info(
                url, download=False
            )
        except ExtractorError:
            vid_data = {"title": url, "uploader": "Jmthon", "formats": []}
        startTime = time()
        retcode = await _mp3Dl(url=url, starttime=startTime, uid="320")
        if retcode != 0:
            return await event.edit(str(retcode))
        _fpath = ""
        thumb_pic = None
        for _path in glob.glob(os.path.join(Config.TEMP_DIR, str(startTime), "*")):
            if _path.lower().endswith((".jpg", ".png", ".webp")):
                thumb_pic = _path
            else:
                _fpath = _path
        if not _fpath:
            return await edit_delete(
                catevent, "**- لقد حدث خطأ اثناء التعرف على المعلومات**"
            )
        await catevent.edit(
            f"**يتم التحضير الى رفع المقطع الصوتي:**\
            \n**{vid_data['title']}***"
        )
        attributes, mime_type = get_attributes(str(_fpath))
        ul = io.open(pathlib.Path(_fpath), "rb")
        if thumb_pic is None:
            thumb_pic = str(
                await pool.run_in_thread(download)(
                    await get_ytthumb(get_yt_video_id(url))
                )
            )
        uploaded = await event.client.fast_upload_file(
            file=ul,
            progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                progress(
                    d,
                    t,
                    catevent,
                    startTime,
                    "جار الرفع  .  . ",
                    file_name=os.path.basename(pathlib.Path(_fpath)),
                )
            ),
        )
        ul.close()
        media = types.InputMediaUploadedDocument(
            file=uploaded,
            mime_type=mime_type,
            attributes=attributes,
            force_file=False,
            thumb=await event.client.upload_file(thumb_pic) if thumb_pic else None,
        )
        await event.client.send_file(
            event.chat_id,
            file=media,
            caption=f"<b>File Name : </b><code>{vid_data.get('title', os.path.basename(pathlib.Path(_fpath)))}</code>",
            supports_streaming=True,
            reply_to=reply_to_id,
            parse_mode="html",
        )
        for _path in [_fpath, thumb_pic]:
            os.remove(_path)
    await catevent.delete()


@jmthon.ar_cmd(
    pattern="تحميل(فيديو)(?:\s|$)([\s\S]*)",
    command=("تحميل", plugin_category),
)
async def download_video(event):
    """To download video from YouTube and many other sites."""
    msg = event.pattern_match.group(1)
    rmsg = await event.get_reply_message()
    if not msg and rmsg:
        msg = rmsg.text
    urls = extractor.find_urls(msg)
    if not urls:
        return await edit_or_reply(
            event, "**⌯︙ يرجى الرد على الرسالة او كتابة الرابط اولا**"
        )
    catevent = await edit_or_reply(event, "⌯︙يتم البحث عن المطلوب انتظر")
    reply_to_id = await reply_id(event)
    for url in urls:
        ytdl_data = await ytdl_down(catevent, video_opts, url)
        if ytdl_down is None:
            return
        try:
            f = pathlib.Path("cat_ytv.mp4")
            print(f)
            catthumb = pathlib.Path("cat_ytv.jpg")
            if not os.path.exists(catthumb):
                catthumb = pathlib.Path("cat_ytv.webp")
            if not os.path.exists(catthumb):
                catthumb = None
            await catevent.edit(
                f"**التحضير لرفع الفيديو:**\
                \n**{ytdl_data['title']}**"
            )
            ul = io.open(f, "rb")
            c_time = time()
            attributes, mime_type = await fix_attributes(
                f, ytdl_data, supports_streaming=True
            )
            uploaded = await event.client.fast_upload_file(
                file=ul,
                progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                    progress(
                        d,
                        t,
                        catevent,
                        c_time,
                        "جار الرفع  .  .  :",
                        file_name=ytdl_data["title"],
                    )
                ),
            )
            ul.close()
            media = types.InputMediaUploadedDocument(
                file=uploaded,
                mime_type=mime_type,
                attributes=attributes,
            )
            await event.client.send_file(
                event.chat_id,
                file=media,
                reply_to=reply_to_id,
                caption=f'**Title :** `{ytdl_data["title"]}`',
                thumb=catthumb,
            )
            os.remove(f)
            if catthumb:
                os.remove(catthumb)
        except TypeError:
            await asyncio.sleep(2)
    await event.delete()


@jmthon.ar_cmd(
    pattern="نتائج(?: |$)(\d*)? ?(.*)",
    command=("نتائج", plugin_category),
    info={
        "header": "يمكنك بحث فيديوهات عبر منصة اليوتيوب",
        "description": "يجلب نتائج بحث منصة يوتيوب مع المشاهدات والمدة مع عدد النتائج المطلوبة فإنه يجلب 10 نتائج",
        "examples": [
            "{tr}نتائج <نص>",
            "{tr}نتائج <1-9> <نص>",
        ],
    },
)
async def yt_search(event):
    "Youtube search command"
    if event.is_reply and not event.pattern_match.group(2):
        query = await event.get_reply_message()
        query = str(query.message)
    else:
        query = str(event.pattern_match.group(2))
    if not query:
        return await edit_delete(event, "⌯︙ يرجى الرد على الرسالة او كتابة الرابط اولا")
    video_q = await edit_or_reply(event, "⌯︙يتم البحث عن المطلوب انتظر")
    if event.pattern_match.group(1) != "":
        lim = int(event.pattern_match.group(1))
        if lim <= 0:
            lim = int(10)
    else:
        lim = int(10)
    try:
        full_response = await ytsearch(query, limit=lim)
    except Exception as e:
        return await edit_delete(video_q, str(e), time=10, parse_mode=_format.parse_pre)
    reply_text = f"⌯︙• البحث :\n`{query}`\n\n⌯︙•  نتائج :\n{full_response}"
    await edit_or_reply(video_q, reply_text)
