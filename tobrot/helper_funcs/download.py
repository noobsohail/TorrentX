#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) gautamajay52 | Shrimadhav U K

import asyncio
import logging
import math
import os
import re
import subprocess
import time
from datetime import datetime
from pathlib import Path

from pyrogram import Client, filters
from tobrot import DOWNLOAD_LOCATION, LOGGER, TELEGRAM_LEECH_UNZIP_COMMAND
from tobrot.helper_funcs.create_compressed_archive import unzip_me, get_base_name
from tobrot.helper_funcs.display_progress import Progress
from tobrot.helper_funcs.upload_to_tg import upload_to_gdrive


async def down_load_media_f(client, message):
    user_command = message.command[0]
    user_id = message.from_user.id
    LOGGER.info(user_id)
    mess_age = await message.reply_text("...", quote=True)
    if not os.path.isdir(DOWNLOAD_LOCATION):
        os.makedirs(DOWNLOAD_LOCATION)
    if message.reply_to_message is not None:
        start_t = datetime.now()
        download_location = str(Path().resolve()) + "/"
        c_time = time.time()
        prog = Progress(user_id, client, mess_age)
        try:
            the_real_download_location = await client.download_media(
                message=message.reply_to_message,
                file_name=download_location,
                progress=prog.progress_for_pyrogram,
                progress_args=("🔄 ᴛʀʏɪɴɢ ᴛᴏ ᴅᴏᴡɴʟᴏᴀᴅ", c_time),
            )
        except Exception as g_e:
            await mess_age.edit(str(g_e))
            LOGGER.error(g_e)
            return
        end_t = datetime.now()
        ms = (end_t - start_t).seconds
        LOGGER.info(the_real_download_location)
        await asyncio.sleep(10)
        if the_real_download_location:
            await mess_age.edit_text(
                f"📥 ᴅᴏᴡɴʟᴏᴀᴅᴇᴅ ᴛᴏ\n<code>{the_real_download_location}</code>\n<u>{ms}</u> sᴇᴄᴏɴᴅ"
            )
        else:
            await mess_age.edit_text("🔴ᴅᴏᴡɴʟᴏᴀᴅ ᴄᴀɴᴄᴇʟʟᴇᴅ ᴏʀ sᴏᴍᴇᴛʜɪɴɢ ʜᴀᴘᴘᴇɴᴇᴅ🔴")
            return
        the_real_download_location_g = the_real_download_location
        if user_command == TELEGRAM_LEECH_UNZIP_COMMAND.lower():
            try:
                check_ifi_file = get_base_name(the_real_download_location)
                file_up = await unzip_me(the_real_download_location)
                if os.path.exists(check_ifi_file):
                    the_real_download_location_g = file_up
            except Exception as ge:
                LOGGER.info(ge)
                LOGGER.info(
                    f"🔴 ᴄᴀɴ'ᴛ ᴇxᴛʀᴀᴄᴛ\n{os.path.basename(the_real_download_location)}"
                )
        await upload_to_gdrive(the_real_download_location_g, mess_age, message, user_id)
    else:
        await mess_age.edit_text(
            "ʀᴇᴘʟʏ ᴛᴏ ᴛᴇʟᴇɢʀᴀᴍ ғɪʟᴇ ғᴏʀ ᴜᴘʟᴏᴀᴅɪɴɢ ᴀᴛ ᴄʟᴏᴜᴅ"
        )


async def download_tg(client, message):
    user_id = message.from_user.id
    LOGGER.info(user_id)
    mess_age = await message.reply_text("...", quote=True)
    if not os.path.isdir(DOWNLOAD_LOCATION):
        os.makedirs(DOWNLOAD_LOCATION)
    if message.reply_to_message is not None:
        start_t = datetime.now()
        download_location = str(Path("./").resolve()) + "/"
        c_time = time.time()
        prog = Progress(user_id, client, mess_age)
        try:
            the_real_download_location = await client.download_media(
                message=message.reply_to_message,
                file_name=download_location,
                progress=prog.progress_for_pyrogram,
                progress_args=("🔄 ᴛʀʏɪɴɢ ᴛᴏ ᴅᴏᴡɴʟᴏᴀᴅ", c_time),
            )
        except Exception as g_e:
            await mess_age.edit(str(g_e))
            LOGGER.error(g_e)
            return
        end_t = datetime.now()
        ms = (end_t - start_t).seconds
        LOGGER.info(the_real_download_location)
        await asyncio.sleep(5)
        if the_real_download_location:
            await mess_age.edit_text(
                f"📥 ᴅᴏᴡɴʟᴏᴀᴅᴇᴅ ᴛᴏ\n<code>{the_real_download_location}</code>\n<u>{ms}</u> sᴇᴄᴏɴᴅ"
            )
        else:
            await mess_age.edit_text("🔴ᴅᴏᴡɴʟᴏᴀᴅ ᴄᴀɴᴄᴇʟʟᴇᴅ ᴏʀ sᴏᴍᴇᴛʜɪɴɢ ʜᴀᴘᴘᴇɴᴇᴅ🔴")
            return
    return the_real_download_location, mess_age
