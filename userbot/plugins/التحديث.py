import asyncio
import os
import sys
from asyncio.exceptions import CancelledError

import heroku3
import requests
import urllib3
from git import Repo
from git.exc import GitCommandError, InvalidGitRepositoryError, NoSuchPathError

from userbot import HEROKU_APP, UPSTREAM_REPO_URL, jmthon

from ..Config import Config
from ..core.logger import logging
from ..core.managers import edit_delete, edit_or_reply
from ..sql_helper.global_collection import (
    add_to_collectionlist,
    del_keyword_collectionlist,
    get_collectionlist_items,
)

lb_info = "https://raw.githubusercontent.com/jmthonar/userbot1/master/jmthon-info.json"


async def ld_info(lb_info):
    infos = requests.get(lb_info).json()
    _version = infos["JMTHON-INFO"]["version"]
    _release = infos["JMTHON-INFO"]["release-date"]
    _branch = infos["JMTHON -INFO"]["branch"]
    _author = infos["JMTHON-INFO"]["author"]
    _auturl = infos["JMTHON-INFO"]["author-url"]
    return _version, _release, _branch, _author, _auturl

cmdhd = Config.COMMAND_HAND_LER

LOGS = logging.getLogger(__name__)
# -- Constants -- #

HEROKU_APP_NAME = Config.HEROKU_APP_NAME or None
HEROKU_API_KEY = Config.HEROKU_API_KEY or None
Heroku = heroku3.from_key(Config.HEROKU_API_KEY)
heroku_api = "https://api.heroku.com"

UPSTREAM_REPO_BRANCH = Config.UPSTREAM_REPO_BRANCH

REPO_REMOTE_NAME = "temponame"
IFFUCI_ACTIVE_BRANCH_NAME = "master"
NO_HEROKU_APP_CFGD = "no heroku application found, but a key given? 😕 "
HEROKU_GIT_REF_SPEC = "HEAD:refs/heads/master"
RESTARTING_APP = "re-starting heroku application"
IS_SELECTED_DIFFERENT_BRANCH = (
    "looks like a custom branch {branch_name} "
    "is being used:\n"
    "in this case, Updater is unable to identify the branch to be updated."
    "please check out to an official branch, and re-start the updater."
)


# -- Constants End -- #

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

requirements_path = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "requirements.txt"
)


async def gen_chlog(repo, diff):
    d_form = "%d/%m/%y"
    return "".join(
        f"  • {c.summary} ({c.committed_datetime.strftime(d_form)}) <{c.author}>\n"
        for c in repo.iter_commits(diff)
    )


async def print_changelogs(event, ac_br, changelog):
    changelog_str = (
        f"**❃ تحديث جديد متاح للسورس:\n\n❃ التغييرات:**\n`{changelog}`"
    )
    if len(changelog_str) > 4096:
        await event.edit("**₰ التغييرات كبيره جدا لذلك تم عمل ملف لها**")
        with open("output.txt", "w+") as file:
            file.write(changelog_str)
        await event.client.send_file(
            event.chat_id,
            "output.txt",
            reply_to=event.id,
        )
        os.remove("output.txt")
    else:
        await event.client.send_message(
            event.chat_id,
            changelog_str,
            reply_to=event.id,
        )
    return True


async def update_requirements():
    reqs = str(requirements_path)
    try:
        process = await asyncio.create_subprocess_shell(
            " ".join([sys.executable, "-m", "pip", "install", "-r", reqs]),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        await process.communicate()
        return process.returncode
    except Exception as e:
        return repr(e)


async def update(event, repo, ups_rem, ac_br):
    try:
        ups_rem.pull(ac_br)
    except GitCommandError:
        repo.git.reset("--hard", "FETCH_HEAD")
    await update_requirements()
    JMTHON = await event.edit(
        "**⌔∮ تم بنجاح تحديث سورس جمثون\n"
        "جار الان اعادة تشغيل البوت انتظر قليلا**"
    )
    await event.client.reload(JMTHON)


async def deploy(event, repo, ups_rem, ac_br, txt):
    if HEROKU_API_KEY is None:
        return await event.edit("**₰ لا يمكنك تحديث السورس الا بوضع فار هيروكو ايبي كي**")
    heroku = heroku3.from_key(HEROKU_API_KEY)
    heroku_applications = heroku.apps()
    if HEROKU_APP_NAME is None:
        await event.edit(
            "**⌔∮ لا يمكنك تحديث جمثون الا بوضع هيروكو ابب نيم**"
            " `HEROKU_APP_NAME`"
        )
        repo.__del__()
        return
    heroku_app = next(
        (app for app in heroku_applications if app.name == HEROKU_APP_NAME),
        None,
    )
    if heroku_app is None:
        await event.edit(
            f"{txt}\n" "**⌔∮ لم يتم التعرف على بيانات تطبيقك في هيروكو لا يمكن التحديث**"
        )
        return repo.__del__()
    JMTHON = await event.edit(
        " ❃ الدينو الان قيد الانتظار يجب عليك الانتظار من 2-3 دقائق للتحديث"
    )
    try:
        ulist = get_collectionlist_items()
        for i in ulist:
            if i == "restart_update":
                del_keyword_collectionlist("restart_update")
    except Exception as e:
        LOGS.error(e)
    try:
        add_to_collectionlist("restart_update", [JMTHON.chat_id, JMTHON.id])
    except Exception as e:
        LOGS.error(e)
    ups_rem.fetch(ac_br)
    repo.git.reset("--hard", "FETCH_HEAD")
    heroku_git_url = heroku_app.git_url.replace("https://", f"https://api:{HEROKU_API_KEY}@")
    if "heroku" in repo.remotes:
        remote = repo.remote("heroku")
        remote.set_url(heroku_git_url)
    else:
        remote = repo.create_remote("heroku", heroku_git_url)
    try:
        remote.push(refspec="HEAD:refs/heads/master", force=True)
    except Exception as error:
        await event.edit(f"{txt}\n**نص الخطأ:**\n`{error}`")
        return repo.__del__()
    build_status = heroku_app.builds(order_by="created_at", sort="desc")[0]
    if build_status.status == "failed":
        return await edit_delete(
            event, "**₰ فشل في اكمال التحديث يبدو انه تم الغاء عمليه التحديث**"
        )
    try:
        remote.push("master:main", force=True)
    except Exception as error:
        await event.edit(f"{txt}\n**⌔∮ هذا هو الخطأ الخاص بك:**\n`{error}`")
        return repo.__del__()
    await event.edit("⪼ فشل تحديث السورس لذلك قم باعادة التشغيل يدويا")
    try:
        await event.client.disconnect()
        if HEROKU_APP is not None:
            HEROKU_APP.restart()
    except CancelledError:
        pass


@jmthon.ar_cmd(pattern="تحديث(| الان)?$")
async def upstream(event):
    conf = event.pattern_match.group(1).strip()
    event = await edit_or_reply(event, "**❃ جار البحث عن التحديثات انتظر قليلا**")
    off_repo = UPSTREAM_REPO_URL
    _version, _release, _branch, _author, _auturl = await ld_info(lb_info)
    force_update = False
    if HEROKU_API_KEY is None or HEROKU_APP_NAME is None:
        return await edit_or_reply(
            event,
            "⪼ يجب عليك وضع الفارات المطلوبة [اضغط هنا](https://t.me/RRRDF/111?single)`",
        )
    try:
        txt = (
            " **❃ عذرا لا يمكن التحديث الان بسبب خطأ غير معروف\n "
            + "لوغتراس:**\n"
        )
        repo = Repo()
    except NoSuchPathError as error:
        await event.edit(f"{txt}\nخطأ {error} ")
        return repo.__del__()
    except GitCommandError as error:
        await event.edit(f"{txt}\n**فشل مبكر {error}**")
        return repo.__del__()
    except InvalidGitRepositoryError as error:
        if conf is None:
            return await event.edit(
                f"**❃ عليك التحديث عبر الامر** : `.تحديث الان`"
            )
        repo = Repo.init()
        origin = repo.create_remote("upstream", off_repo)
        origin.fetch()
        force_update = True
        repo.create_head("master", origin.refs.master)
        repo.heads.master.set_tracking_branch(origin.refs.master)
        repo.heads.master.checkout(True)
    ac_br = repo.active_branch.name
    if ac_br != UPSTREAM_REPO_BRANCH:
        await event.edit(
            "**[UPDATER]:**\n"
            f"- ({ac_br}). "
        )
        return repo.__del__()
    try:
        repo.create_remote("upstream", off_repo)
    except BaseException:
        pass
    ups_rem = repo.remote("upstream")
    ups_rem.fetch(ac_br)
    changelog = await gen_chlog(repo, f"HEAD..upstream/{ac_br}")
    if changelog == "" and not force_update:
        await event.edit(
            f"<b><i>تحديث سورس جمثون</b></i> \n\n<b><i><u>معلومات التحديث :</b></i></u> \n<b>• الفرع :</b> {_branch} \n<b>• تاريخ التحديث :</b> {_release} \n<b>• الاصدار :</b> {_version} \n<b>• المطور :</b> <a href='{_auturl}'>{_author}</a>",
            link_preview=False,
            parse_mode="HTML",
        )
        """await event.edit(
            "\n⌔∮ سورس جمثون الان مع اخر اصدار"
            f"**{UPSTREAM_REPO_BRANCH}**\n"
        )"""
        return repo.__del__()
    if conf == "" and not force_update:
        await print_changelogs(event, ac_br, changelog)
        await event.delete()
        return await event.respond(
            f"⌔∮ تم العثور على تحديث لسورس جمثون للتحديث  ؛ `{cmdhd}تحديث جمثون` "
        )
    if force_update:
        await event.edit(
            " **⌔∮ جار المزامنه مع اخر تحديث مستقر انتظر قليلا**"
        )
    if conf == "الان":
        await event.edit("**⌔∮ جارِ تحديث جمثون عليك الانتظار**")
        await update(event, repo, ups_rem, ac_br)
    return


@jmthon.ar_cmd(pattern="تحديث جمثون$")
async def upstream(event):
    event = await edit_or_reply(event, "**⪼ يتم الان تحديث سورس جمثون يرجى الانتظار**")
    off_repo = "https://github.com/jmthonar/jmthon"
    os.chdir("/app")
    try:
        txt = (
            " **❃ عذرا لا يمكن التحديث الان بسبب خطأ غير معروف\n "
            + "لوغتراس:**\n"
        )

        repo = Repo()

    except NoSuchPathError as error:
        await event.edit(f"{txt}\nلقد حدث خطأ لم يتم العثور على {error}")
        return repo.__del__()
    except GitCommandError as error:
        await event.edit(f"{txt}\n₰ فشل مبكر {error}`")
        return repo.__del__()
    except InvalidGitRepositoryError:
        repo = Repo.init()
        origin = repo.create_remote("upstream", off_repo)
        origin.fetch()
        repo.create_head("master", origin.refs.master)
        repo.heads.master.set_tracking_branch(origin.refs.master)
        repo.heads.master.checkout(True)
    try:
        repo.create_remote("upstream", off_repo)
    except BaseException:
        pass
    ac_br = repo.active_branch.name
    ups_rem = repo.remote("upstream")
    ups_rem.fetch(ac_br)
    await event.edit("**❃ جار التحديث انتظر قليلا**")
    await deploy(event, repo, ups_rem, ac_br, txt)

# @Jmthon - < https://t.me/jmthon >
