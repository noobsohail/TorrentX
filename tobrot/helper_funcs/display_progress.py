#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K | gautamajay52

import logging
import math
import os
import time

from pyrogram.errors.exceptions import FloodWait
from tobrot import (
    EDIT_SLEEP_TIME_OUT,
    FINISHED_PROGRESS_STR,
    UN_FINISHED_PROGRESS_STR,
    gDict,
    LOGGER,
)
from pyrogram import Client

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message


class Progress:
    def __init__(self, from_user, client, mess: Message):
        self._from_user = from_user
        self._client = client
        self._mess = mess
        self._cancelled = False

    @property
    def is_cancelled(self):
        chat_id = self._mess.chat.id
        mes_id = self._mess.message_id
        if gDict[chat_id] and mes_id in gDict[chat_id]:
            self._cancelled = True
        return self._cancelled

    async def progress_for_pyrogram(self, current, total, ud_type, start):
        chat_id = self._mess.chat.id
        mes_id = self._mess.message_id
        from_user = self._from_user
        now = time.time()
        diff = now - start
        reply_markup = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "❌ ᴄᴀɴᴄᴇʟ",
                        callback_data=(
                            f"gUPcancel/{chat_id}/{mes_id}/{from_user}"
                        ).encode("UTF-8"),
                    )
                ]
            ]
        )
        if self.is_cancelled:
            LOGGER.info("stopping ")
            await self._mess.edit(
                f"🔴 ʟᴇᴇᴄʜ ᴄᴀɴᴄᴇʟʟᴇᴅ: `{ud_type}` ({humanbytes(total)})"
            )
            await self._client.stop_transmission()

        if round(diff % float(EDIT_SLEEP_TIME_OUT)) == 0 or current == total:
            # if round(current / total * 100, 0) % 5 == 0:
            percentage = current * 100 / total
            speed = current / diff
            elapsed_time = round(diff) * 1000
            time_to_completion = round((total - current) / speed) * 1000
            estimated_total_time = time_to_completion

            elapsed_time = TimeFormatter(milliseconds=elapsed_time)
            estimated_total_time = TimeFormatter(milliseconds=estimated_total_time)

            progress = "\n[{0}{1}] \n\n💯 ᴘʀᴏɢʀᴇss: {2}%\n⚙️ ᴇɴɢɪɴᴇ: ᴘʏʀᴏɢʀᴀᴍ\n".format(
                "".join(
                    [FINISHED_PROGRESS_STR for i in range(math.floor(percentage / 10))]
                ),
                "".join(
                    [
                        UN_FINISHED_PROGRESS_STR
                        for i in range(10 - math.floor(percentage / 10))
                    ]
                ),
                round(percentage, 2),
            )

            tmp = progress + "✅ ᴅᴏɴᴇ: {0}\n💾 ᴛᴏᴛᴀʟ ғɪʟᴇ sɪᴢᴇ : {1}\n⚡ sᴘᴇᴇᴅ: {2}/s\n⏰ ᴇᴛᴀ: {3}\n\n".format(
                humanbytes(current),
                humanbytes(total),
                humanbytes(speed),
                # elapsed_time if elapsed_time != '' else "0 s",
                estimated_total_time if estimated_total_time != "" else "0 s",
            )
            try:
                if not self._mess.photo:
                    await self._mess.edit_text(
                        text="{}\n {}".format(ud_type, tmp), reply_markup=reply_markup
                    )
                else:
                    await self._mess.edit_caption(
                        caption="{}\n {}".format(ud_type, tmp)
                    )
            except FloodWait as fd:
                logger.warning(f"{fd}")
                time.sleep(fd.x)
            except Exception as ou:
                logger.info(ou)


def humanbytes(size):
    # https://stackoverflow.com/a/49361727/4723940
    # 2**10 = 1024
    if not size:
        return ""
    power = 2 ** 10
    n = 0
    Dic_powerN = {0: " ", 1: "ᴋ", 2: "ᴍ", 3: "ɢ", 4: "ᴛ"}
    while size > power:
        size /= power
        n += 1
    return str(round(size, 2)) + " " + Dic_powerN[n] + "ʙ"


def TimeFormatter(milliseconds: int) -> str:
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = (
        ((str(days) + "ᴅ, ") if days else "")
        + ((str(hours) + "ʜ, ") if hours else "")
        + ((str(minutes) + "ᴍ, ") if minutes else "")
        + ((str(seconds) + "s, ") if seconds else "")
        + ((str(milliseconds) + "ᴍs, ") if milliseconds else "")
    )
    return tmp[:-2]
