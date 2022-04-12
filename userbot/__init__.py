# @Jmthon - < https://t.me/Jmthon >
# Copyright (C) 2021 - JMTHON-AR
# All rights reserved.
#
# This file is a part of < https://github.com/JMTHON-AR/JMTHON >
# Please read the GNU Affero General Public License in;
# < https://github.com/JMTHON-AR/JM-THON/blob/master/LICENSE
# ===============================================================
import signal
import sys
import time
import heroku3
import logging
import os
import re
import sys
import time
from asyncio import get_event_loop
from base64 import b64decode
from distutils.util import strtobool as sb
from logging import DEBUG, INFO, basicConfig, getLogger


from pySmartDL import SmartDL
from pytgcalls import PyTgCalls
from telethon.network.connection.tcpabridged import ConnectionTcpAbridged
from telethon.sessions import StringSession
from telethon.sync import TelegramClient, custom, events
from .Config import Config
from .core.logger import logging
from .helpers.utils.utils import runasync
from telethon.sessions import StringSession
from telethon.sync import TelegramClient, custom, events
from .sql_helper.globals import addgvar, delgvar, gvarstatus

__version__ = "3.0.6"
__license__ = "رخصة جنو أفيرو العمومية v3.0"
__author__ = "jmthon <https://github.com/jmthonar/userbot>"
__copyright__ = f"حقوق جمثون (C) 2020 - 2021  {__author__}"

jmthon.version = __version__
jmthon.tgbot.version = __version__
LOGS = logging.getLogger("jmthon")
bot = jmthon

StartTime = time.time()
jmthonversion = "3.0.6"


def close_connection(*_):
    print("تم اغلاق اتصال السورس.")
    runasync(jmthon.disconnect())
    sys.exit(143)


signal.signal(signal.SIGTERM, close_connection)

if Config.UPSTREAM_REPO == "jmthonrz":
    UPSTREAM_REPO_URL = "https://github.com/jmthonar/userbot"
else:
    UPSTREAM_REPO_URL = Config.UPSTREAM_REPO

if Config.PRIVATE_GROUP_BOT_API_ID == 0:
    if gvarstatus("PRIVATE_GROUP_BOT_API_ID") is None:
        Config.BOTLOG = False
        Config.BOTLOG_CHATID = "me"
    else:
        Config.BOTLOG_CHATID = int(gvarstatus("PRIVATE_GROUP_BOT_API_ID"))
        Config.PRIVATE_GROUP_BOT_API_ID = int(gvarstatus("PRIVATE_GROUP_BOT_API_ID"))
        Config.BOTLOG = True
else:
    if str(Config.PRIVATE_GROUP_BOT_API_ID)[0] != "-":
        Config.BOTLOG_CHATID = int("-" + str(Config.PRIVATE_GROUP_BOT_API_ID))
    else:
        Config.BOTLOG_CHATID = Config.PRIVATE_GROUP_BOT_API_ID
    Config.BOTLOG = True

if Config.PM_LOGGER_GROUP_ID == 0:
    if gvarstatus("PM_LOGGER_GROUP_ID") is None:
        Config.PM_LOGGER_GROUP_ID = -100
    else:
        Config.PM_LOGGER_GROUP_ID = int(gvarstatus("PM_LOGGER_GROUP_ID"))
elif str(Config.PM_LOGGER_GROUP_ID)[0] != "-":
    Config.PM_LOGGER_GROUP_ID = int("-" + str(Config.PM_LOGGER_GROUP_ID))

try:
    if Config.HEROKU_API_KEY is not None or Config.HEROKU_APP_NAME is not None:
        HEROKU_APP = heroku3.from_key(Config.HEROKU_API_KEY).apps()[
            Config.HEROKU_APP_NAME
        ]
    else:
        HEROKU_APP = None
except Exception:
    HEROKU_APP = None

if STRING_SESSION:
    session = StringSession(str(STRING_SESSION))
else:
    session = "jmthonbot"
try:
    jmthon = TelegramClient(
        session=session,
        api_id=API_KEY,
        api_hash=API_HASH,
        connection=ConnectionTcpAbridged,
        auto_reconnect=True,
        connection_retries=None,
    )
    call_py = PyTgCalls(jmthon)
except Exception as e:
    print(f"STRING_SESSION - {e}")
    sys.exit()

if STRING_2:
    session2 = StringSession(str(STRING_2))
    JMTHON2 = TelegramClient(
        session=session2,
        api_id=API_KEY,
        api_hash=API_HASH,
        connection=ConnectionTcpAbridged,
        auto_reconnect=True,
        connection_retries=None,
    )
    call_py2 = PyTgCalls(JMTHON2)
else:
    call_py2 = None
    JMTHON2 = None


if STRING_3:
    session3 = StringSession(str(STRING_3))
    JMTHON3 = TelegramClient(
        session=session3,
        api_id=API_KEY,
        api_hash=API_HASH,
        connection=ConnectionTcpAbridged,
        auto_reconnect=True,
        connection_retries=None,
    )
    call_py3 = PyTgCalls(JMTHON3)
else:
    call_py3 = None
    JMTHON3 = None


if STRING_4:
    session4 = StringSession(str(STRING_4))
    JMTHON4 = TelegramClient(
        session=session4,
        api_id=API_KEY,
        api_hash=API_HASH,
        connection=ConnectionTcpAbridged,
        auto_reconnect=True,
        connection_retries=None,
    )
    call_py4 = PyTgCalls(JMTHON4)
else:
    call_py4 = None
    JMTHON4 = None


if STRING_5:
    session5 = StringSession(str(STRING_5))
    JMTHON5 = TelegramClient(
        session=session5,
        api_id=API_KEY,
        api_hash=API_HASH,
        connection=ConnectionTcpAbridged,
        auto_reconnect=True,
        connection_retries=None,
    )
    call_py5 = PyTgCalls(JMTHON5)
else:
    call_py5 = None
    JMTHON5 = None


# Global Configiables
COUNT_MSG = 0
USERS = {}
COUNT_PM = {}
LASTMSG = {}
CMD_HELP = {}
ISAFK = False
AFKREASON = None
CMD_LIST = {}
SUDO_LIST = {}
# for later purposes
INT_PLUG = ""
LOAD_PLUG = {}

# Variables
BOTLOG = Config.BOTLOG
BOTLOG_CHATID = Config.BOTLOG_CHATID
PM_LOGGER_GROUP_ID = Config.PM_LOGGER_GROUP_ID
