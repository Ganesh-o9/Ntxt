from pyrogram.errors.exceptions.bad_request_400 import StickerEmojiInvalid
import requests
import json
import subprocess
import pyrogram
from pyrogram import Client, filters
from pyrogram.types.messages_and_media import message
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import FloodWait
from pyromod import listen
from pyrogram.types import Message

from pyrogram import Client, filters
import tgcrypto
from p_bar import progress_bar
from details import api_id, api_hash, bot_token, sudo_groups
from subprocess import getstatusoutput
import helper
import logging
import time
from aiohttp import ClientSession
import asyncio
import aiofiles
from pyrogram.types import User, Message
# import progressor
# from progressor import progress_for_pyrogram
import sys
import re
import os
# import pycurl
# By... heArtðŸ–¤
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Language': 'en-US,en;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Referer': 'http://www.visionias.in/',
    'Sec-Fetch-Dest': 'iframe',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'cross-site',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 12; RMX2121) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36',
    'sec-ch-ua': '"Chromium";v="107", "Not=A?Brand";v="24"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"Android"',
}

# quality dict
visionias_quality_dict = {
    "144": "164000",
    "240": "234000",
    "360": "314000",
    "480": "414000",
    "720": "696000",
}

visionias_url_extract_pattern = r"(https://.*?playlist.m3u8.*?)\""

bot = Client(

    "bot",
    api_id=api_id,
    api_hash=api_hash,
    bot_token=bot_token)

# bot = Client(
#    "bot",
#    bot_token=os.environ.get("BOT_TOKEN"),
#    api_id=int(os.environ.get("API_ID")),
#    api_hash=os.environ.get("API_HASH")
# )
# auth_users = [ int(chat) for chat in os.environ.get("AUTH_USERS").split(",") if chat != '']
# sudo_users = auth_users
# sudo_groups = [ int(chat) for chat in os.environ.get("GROUPS").split(",")  if chat != '']


@bot.on_message(filters.command(["start"]) & (filters.chat(sudo_groups)))
async def account_login(bot: Client, m: Message):

    editable = await m.reply_text("**Hellow deAr,** i am here for multipurpose & in **under construction.**\n\n**Developer:** Smile Bhai \n**Language:** Python\n\n**All running commands are:-**\n\n/txt\n/adda_pdf\n/jw\n/heArt\n/top\n/cw\n/pw\n\n**BOT IS IN  UNDERCONSTRUCTION.**\n")


@bot.on_message(filters.command(["cancel"]) & (filters.chat(sudo_groups)))
async def cancel(_, m):
    editable = await m.reply_text("Canceling All process Plz wait")
    global cancel
    cancel = True
    await editable.edit("cancled😡", True)
    return


@bot.on_message(filters.command("restart") & (filters.chat(sudo_groups)))
async def restart_handler(_, m):
    await m.reply_text("Restarted!🙄", True)
    os.execl(sys.executable, sys.executable, *sys.argv)


@bot.on_message(filters.command(["txt"]) & (filters.chat(sudo_groups)))
async def account_login(bot: Client, m: Message):

    editable = await m.reply_text(" **Hello DeAr,** I am Text Downloader Bot.\nI can download videos from text file one by one.\n\n**Developer: Smile Bhai** \n**Language:** Python\n**Framework:** 🔥Pyrogram\n\nNow Send Your **TXT File:-**\n")
    input: Message = await bot.listen(editable.chat.id)
    x = await input.download()
    await input.delete(True)

    path = f"./downloads/{m.chat.id}"

    try:
        with open(x, "r") as f:
            content = f.read()
        content = content.split("\n")
        links = []
        for i in content:
            links.append(i.split(":", 1))
        os.remove(x)
        # print(len(links))
    except:
        await m.reply_text("Invalid file input.🥲")
        os.remove(x)
        return

    editable = await m.reply_text(f"Total links found are **{len(links)}**\n\nSend From where you want to download initial is **0**")
    input1: Message = await bot.listen(editable.chat.id)
    raw_text = input1.text

    try:
        arg = int(raw_text)
    except:
        arg = 0

    editable = await m.reply_text("**Enter Batch Name**")
    input0: Message = await bot.listen(editable.chat.id)
    raw_text0 = input0.text

    await m.reply_text("**Enter resolution**")
    input2: Message = await bot.listen(editable.chat.id)
    raw_text2 = input2.text

    editable4 = await m.reply_text("Now send the **Thumb url**\nEg : ```https://telegra.ph/file/1c2a10e73e22774c5ce0e.jpg```\n\nor Send **no**")
    input6 = message = await bot.listen(editable.chat.id)
    raw_text6 = input6.text

    thumb = input6.text
    if thumb.startswith("http://") or thumb.startswith("https://"):
        getstatusoutput(f"wget '{thumb}' -O 'thumb.jpg'")
        thumb = "thumb.jpg"
    else:
        thumb == "no"

    if raw_text == '0':
        count = 1
    else:
        count = int(raw_text)

    try:
        for i in range(arg, len(links)):

            url = links[i][1]
            if "visionias" in url:
                async with ClientSession() as session:
                    async with session.get(url, headers=headers) as resp:
                        text = await resp.text()
                        url = re.search(
                            visionias_url_extract_pattern, text).group(1)

            name1 = links[i][0].replace("\t", "").replace(":", "").replace("/", "").replace("+", "").replace(
                "#", "").replace("|", "").replace("@", "").replace("*", "").replace(".", "").strip()

            if raw_text2 == "144":

                cmd = f'yt-dlp -F "{url}"'
                k = await helper.run(cmd)
                out = helper.vid_info(str(k))
                # print(out)
                if '256x144' in out:
                    ytf = f"{out['256x144']}"
                elif '320x180' in out:
                    ytf = out['320x180']
                elif 'unknown' in out:
                    ytf = out["unknown"]
                else:
                    for data1 in out:
                        ytf = out[data1]
            elif raw_text2 == "180":

                cmd = f'yt-dlp -F "{url}"'
                k = await helper.run(cmd)
                out = helper.vid_info(str(k))
                # print(out)
                if '320x180' in out:
                    ytf = out['320x180']
                elif '426x240' in out:
                    ytf = out['426x240']
                elif 'unknown' in out:
                    ytf = out["unknown"]
                else:
                    for data2 in out:
                        ytf = out[data2]
            elif raw_text2 == "240":

                cmd = f'yt-dlp -F "{url}"'
                k = await helper.run(cmd)
                out = helper.vid_info(str(k))
                # print(out)
                if '426x240' in out:
                    ytf = out['426x240']
                elif '426x234' in out:
                    ytf = out['426x234']
                elif '480x270' in out:
                    ytf = out['480x270']
                elif '480x272' in out:
                    ytf = out['480x272']
                elif '640x360' in out:
                    ytf = out['640x360']
                elif 'unknown' in out:
                    ytf = out["unknown"]
                else:
                    for data3 in out:
                        ytf = out[data3]
            elif raw_text2 == "360":

                cmd = f'yt-dlp -F "{url}"'
                k = await helper.run(cmd)
                out = helper.vid_info(str(k))
                # print(out)
                if '640x360' in out:
                    ytf = out['640x360']
                elif '638x360' in out:
                    ytf = out['638x360']
                elif '636x360' in out:
                    ytf = out['636x360']
                elif '768x432' in out:
                    ytf = out['768x432']
                elif '638x358' in out:
                    ytf = out['638x358']
                elif '852x316' in out:
                    ytf = out['852x316']
                elif '850x480' in out:
                    ytf = out['850x480']
                elif '848x480' in out:
                    ytf = out['848x480']
                elif '854x480' in out:
                    ytf = out['854x480']
                elif '852x480' in out:
                    ytf = out['852x480']
                elif '854x470' in out:
                    ytf = out['852x470']
                elif 'unknown' in out:
                    ytf = out["unknown"]
                else:
                    for data4 in out:
                        ytf = out[data4]
            elif raw_text2 == "480":

                cmd = f'yt-dlp -F "{url}"'
                k = await helper.run(cmd)
                out = helper.vid_info(str(k))
                # print(out)
                if '854x480' in out:
                    ytf = out['854x480']
                elif '852x480' in out:
                    ytf = out['852x480']
                elif '854x470' in out:
                    ytf = out['854x470']
                elif '768x432' in out:
                    ytf = out['768x432']
                elif '848x480' in out:
                    ytf = out['848x480']
                elif '850x480' in out:
                    ytf = ['850x480']
                elif '960x540' in out:
                    ytf = out['960x540']
                elif '640x360' in out:
                    ytf = out['640x360']
                elif 'unknown' in out:
                    ytf = out["unknown"]
                else:
                    for data5 in out:
                        ytf = out[data5]

            elif raw_text2 == "720":

                cmd = f'yt-dlp -F "{url}"'
                k = await helper.run(cmd)
                out = helper.vid_info(str(k))
                # print(out)
                if '1280x720' in out:
                    ytf = out['1280x720']
                elif '1280x704' in out:
                    ytf = out['1280x704']
                elif '1280x474' in out:
                    ytf = out['1280x474']
                elif '1920x712' in out:
                    ytf = out['1920x712']
                elif '1920x1056' in out:
                    ytf = out['1920x1056']
                elif '854x480' in out:
                    ytf = out['854x480']
                elif '640x360' in out:
                    ytf = out['640x360']
                elif 'unknown' in out:
                    ytf = out["unknown"]
                else:
                    for data6 in out:
                        ytf = out[data6]
            elif "player.vimeo" in url:
                if raw_text2 == '144':
                    ytf = 'http-240p'
                elif raw_text2 == "240":
                    ytf = 'http-240p'
                elif raw_text2 == '360':
                    ytf = 'http-360p'
                elif raw_text2 == '480':
                    ytf = 'http-540p'
                elif raw_text2 == '720':
                    ytf = 'http-720p'
                else:
                    ytf = 'http-360p'
            else:
                cmd = f'yt-dlp -F "{url}"'
                k = await helper.run(cmd)
                out = helper.vid_info(str(k))
                for dataS in out:
                    ytf = out[dataS]

            try:
                if "unknown" in out:
                    res = "NA"
                else:
                    res = list(out.keys())[list(out.values()).index(ytf)]

                name = f'{str(count).zfill(3)}) {name1} {res}'
            except Exception:
                res = "NA"

            # if "youtu" in url:
            # if ytf == f"'bestvideo[height<={raw_text2}][ext=mp4]+bestaudio[ext=m4a]'" or "acecwply" in url:
            if "acecwply" in url:
                cmd = f'yt-dlp -o "{name}.%(ext)s" -f "bestvideo[height<={raw_text2}]+bestaudio" --hls-prefer-ffmpeg --no-keep-video --remux-video mkv --no-warning "{url}"'
            elif "youtu" in url:
                cmd = f'yt-dlp -i -f "bestvideo[height<={raw_text2}]+bestaudio" --no-keep-video --remux-video mkv --no-warning "{url}" -o "{name}.%(ext)s"'
            elif "player.vimeo" in url:
                cmd = f'yt-dlp -f "{ytf}+bestaudio" --no-keep-video --remux-video mkv "{url}" -o "{name}.%(ext)s"'
            elif "aes128" in url:
            	cmd = f'yt-dlp -f "bestvideo[height<={int(raw_text2)}]+bestaudio" --no-keep-video --remux-video mkv "{url}" -o "{name}.%(ext)s"'
            elif "m3u8" or "livestream" in url:
                cmd = f'yt-dlp -f "{ytf}" --no-keep-video --remux-video mkv "{url}" -o "{name}.%(ext)s"'
            elif ytf == "0" or "unknown" in out:
                cmd = f'yt-dlp -f "{ytf}" --no-keep-video --remux-video mkv "{url}" -o "{name}.%(ext)s"'
            elif ".pdf" in url:
                cmd = "pdf"
            else:
                cmd = f'yt-dlp -f "{ytf}+bestaudio" --hls-prefer-ffmpeg --no-keep-video --remux-video mkv "{url}" -o "{name}.%(ext)s"'

            try:
                Show = f"**Downloading:-**\n**Name :-** `{name}\nQuality - {raw_text2}`\n\n**Url :-**\n`{url}`\n\n"
                prog = await m.reply_text(Show)
                cc = f'{str(count).zfill(3)}.  {name1} {res}.mkv\n\n**Batch:-** {raw_text0}\n\n'
                cc1 = f'{str(count).zfill(3)}. {name1} {res}.pdf\n\n**Batch:-** {raw_text0}\n\n'
#                 if cmd == "pdf" or "drive" in url:
#                     try:
#                         ka=await helper.download(url,name)
#                         await prog.delete (True)
#                         time.sleep(1)
#                         # await helper.send_doc(bot,m,cc,ka,cc1,prog,count,name)
#                         reply = await m.reply_text(f"Uploading - `{name}`\n")
#                         time.sleep(1)
#                         start_time = time.time()
#                         await m.reply_document(ka,caption=cc1)
#                         count+=1
#                         await reply.delete (True)
#                         time.sleep(1)
#                         os.remove(ka)
#                         time.sleep(3)
#                     except FloodWait as e:
#                         await m.reply_text(str(e))
#                         time.sleep(e.x)
#                         continue
                if cmd == "pdf" or ".pdf" in url:
                    try:
                        ka = await helper.aio(url, name)
                        await prog.delete(True)
                        time.sleep(1)
                        reply = await m.reply_text(f"Uploading - ```{name}```\n")
                        time.sleep(1)
                        start_time = time.time()
                        await m.reply_document(ka, caption=f'{str(count).zfill(3)}. {name1} {res}.pdf\n\n**Batch:-** {raw_text0}\n')
                        count += 1
                        # time.sleep(1)
                        await reply.delete(True)
                        time.sleep(1)
                        os.remove(ka)
                        time.sleep(3)
                    except FloodWait as e:
                        await m.reply_text(str(e))
                        time.sleep(e.x)
                        continue
                else:
                    res_file = await helper.download_video(url, cmd, name)
                    filename = res_file
                    await helper.send_vid(bot, m, cc, filename, thumb, name, prog)
                    count += 1
                    time.sleep(1)

            except Exception as e:
                await m.reply_text(f"**downloading failed **\n{str(e)}\n**Name** - {name}\n**Link** - `{url}`\n")
                continue

    except Exception as e:
        await m.reply_text(e)
    await m.reply_text("Done.")


@bot.on_message(filters.command(["top"]) & (filters.chat(sudo_groups)))
async def account_login(bot: Client, m: Message):
    editable = await m.reply_text(f"**Hello DeAr,** I am **TopRankers Downloader Bot.**\nI can download videos from text file one by one.\n\n**Developer: Smile Bhai** \n**Language:** Python\n**Framework:** ðŸ”¥Pyrogram \n\nNow Send Your **TXT File:-**")
    input: Message = await bot.listen(editable.chat.id)
    x = await input.download()
    await input.delete(True)

    try:
        with open(x, "r") as f:
            content = f.read()
        content = content.split("\n")
        links = []
        for i in content:
            links.append(i.split(":", 1))
        os.remove(x)
        # print(len(links))
    except:
        await m.reply_text("Invalid file input.ðŸ¥²")
        os.remove(x)
        return

    editable = await m.reply_text(f"Total links found are **{len(links)}**\n\nSend From where you want to download initial is **0**")
    input1: Message = await bot.listen(editable.chat.id)
    raw_text = input1.text

    try:
        arg = int(raw_text)
    except:
        arg = 0

    editable = await m.reply_text(f"**Copy Paste the App Name of which you want to download videos.**\n\n`vikramjeet`\n\n`sure60`\n\n`theoptimistclasses`")
    input0: Message = await bot.listen(editable.chat.id)
    raw_text0 = input0.text

    editable2 = await m.reply_text("**Enter Batch Name**")
    input5: Message = await bot.listen(editable.chat.id)
    raw_text5 = input5.text

    editable4 = await m.reply_text("Now send the **Thumb url**\nEg : ```https://telegra.ph/file/1c2a10e73e22774c5ce0e.jpg```\n\nor Send **no**")
    input6 = message = await bot.listen(editable.chat.id)
    raw_text6 = input6.text

    thumb = input6.text
    if thumb.startswith("http://") or thumb.startswith("https://"):
        getstatusoutput(f"wget '{thumb}' -O 'thumb.jpg'")
        thumb = "thumb.jpg"
    else:
        thumb == "no"

    if raw_text == '0':
        count = 1
    else:
        count = int(raw_text)

    try:
        for i in range(arg, len(links)):

            url = links[i][1]
            name1 = links[i][0].replace("\t", "").replace("/", "").replace("+", "").replace("#", "").replace(
                "|", "").replace("@", "").replace(":", "").replace("*", "").replace(".", "").strip()
            # await m.reply_text(name +":"+ url)

            # Show = f"**Downloading:-**\n\n**Name :-** ```{name}\nQuality - {raw_text2}```\n\n**Url :-** ```{url}```"
            # prog = await m.reply_text(Show)
            # cc = f'>> **Name :** {name}\n>> **Title :** {raw_text0}\n\n>> **Index :** {count}'

            if raw_text0 in "vikramjeet":

                y = url.replace("/", "%2F")
#                 rout = f"https://www.toprankers.com/?route=common/ajax&mod=liveclasses&ack=getcustompolicysignedcookiecdn&stream=https%3A%2F%2Fsignedsec.toprankers.com%2Flivehttporigin%2F{y[56:-14]}%2Fmaster.m3u8"
                rout = f"https://www.toprankers.com/?route=common/ajax&mod=liveclasses&ack=getcustompolicysignedcookiecdn&stream=https%3A%2F%2Fsignedsec.toprankers.com%2F{y[39:-14]}%2Fmaster.m3u8"
                getstatusoutput(f'curl "{rout}" -c "cookie.txt"')
                cook = "cookie.txt"
                # print (rout)
                # print(url)
            elif raw_text0 in "sure60":
                y1 = url.replace("/", "%2F")
#                 rout = f"https://onlinetest.sure60.com/?route=common/ajax&mod=liveclasses&ack=getcustompolicysignedcookiecdn&stream=https%3A%2F%2Fvodcdn.sure60.com%2Flivehttporigin%2F{y[49:-14]}%2Fmaster.m3u8"
                rout = f"https://onlinetest.sure60.com/?route=common/ajax&mod=liveclasses&ack=getcustompolicysignedcookiecdn&stream=https%3A%2F%2Fvodcdn.sure60.com%2F{y1[32:-14]}%2Fmaster.m3u8"
                getstatusoutput(f'curl "{rout}" -c "cookie.txt"')
                cook = "cookie.txt"
            elif raw_text0 in "theoptimistclasses":
                y = url.replace("/", "%2F")
                rout = f"https://live.theoptimistclasses.com/?route=common/ajax&mod=liveclasses&ack=getcustompolicysignedcookiecdn&stream=https%3A%2F%2Fvodcdn.theoptimistclasses.com%2F{y[44:-14]}%2Fmaster.m3u8"
                getstatusoutput(f'curl "{rout}" -c "cookie.txt"')
                cook = "cookie.txt"

            name = f'{str(count).zfill(3)}) {name1}'
            Show = f"**Downloading:-**\n\n**Name :-** `{name}`\n\n**Url :-** `{url}`\n\n**rout** :- `{rout}`"
            prog = await m.reply_text(Show)
            cc = f'{str(count).zfill(3)}.  {name1} {res}.mp4\n\n**Batch:-** {raw_text0}\n\n'

            cmd = f'yt-dlp -o "{name}.mp4" --cookies {cook} "{url}"'
            try:
                download_cmd = f"{cmd} -R 25 --fragment-retries 25 --external-downloader aria2c --downloader-args 'aria2c: -x 16 -j 32'"
                os.system(download_cmd)
                filename = f"{name}.mp4"
                subprocess.run(
                    f'ffmpeg -i "{filename}" -ss 00:01:00 -vframes 1 "{filename}.jpg"', shell=True)
                await prog.delete(True)
                reply = await m.reply_text(f"Uploading - ```{name}```\n")
                try:
                    if thumb == "no":
                        thumbnail = f"{filename}.jpg"
                    else:
                        thumbnail = thumb
                except Exception as e:
                    await m.reply_text(str(e))

                dur = int(helper.duration(filename))

                start_time = time.time()

                await m.reply_video(f"{name}.mp4", supports_streaming=True, height=720, width=1280, caption=cc, duration=dur, thumb=thumbnail, progress=progress_bar, progress_args=(reply, start_time))
                count += 1
                os.remove(f"{name}.mp4")

                os.remove(f"{filename}.jpg")
                os.remove(cook)
                await reply.delete(True)
                time.sleep(1)
            except Exception as e:
                await m.reply_text(f"**downloading failed âŒ**\n{str(e)}\n**Name** - {name}\n**Link** - `{url}`\n\n**rout** :- `{rout}`")
                continue
    except Exception as e:
        await m.reply_text(str(e))
    await m.reply_text("Done")


@bot.on_message(filters.command(["adda_pdf"]))
async def adda_pdf(bot: Client, m: Message):
    editable = await m.reply_text(f"**Hi im Pdf Adda pdf dl**\n\n**Developer : Smile Bhai**\n**Language:** Python\n**Framework:** ðŸ”¥Pyrogram\n\nNow send your file to download **ADDA PDFs**\n")
    input: Message = await bot.listen(editable.chat.id)
    x = await input.download()
    await input.delete(True)

    try:
        with open(x, "r") as f:
            content = f.read()
        content = content.split("\n")
        links = []
        for i in content:
            links.append(i.split(":", 1))
        os.remove(x)
        # print(len(links))
    except:
        await m.reply_text("Invalid file input.ðŸ¥²")
        os.remove(x)
        return

    editable = await m.reply_text(f"Total links found are **{len(links)}**\n\nSend From where you want to download initial is **0**")
    input1: Message = await bot.listen(editable.chat.id)
    raw_text = input1.text

    try:
        arg = int(raw_text)
    except:
        arg = 0

    editable2 = await m.reply_text("**Enter Token**")
    input5: Message = await bot.listen(editable.chat.id)
    raw_text5 = input5.text

    if raw_text == '0':
        count = 1
    else:
        count = int(raw_text)

    try:
        for i in range(arg, len(links)):

            url = links[i][1]
            name1 = links[i][0].replace("\t", "").replace("/", "").replace("+", "").replace("#", "").replace("|", "").replace(
                "@", "").replace(":", "").replace("*", "").replace(".", "").replace("'", "").replace('"', '').strip()
            name = f'{str(count).zfill(3)} {name1}'
            Show = f"**Downloading:-**\n\n**Name :-** `{name}`\n\n**Url :-** `{url}`"
            prog = await m.reply_text(Show)
            cc = f'{str(count).zfill(3)}. {name1}.pdf\n'
            try:
                getstatusoutput(
                    f'curl --http2 -X GET -H "Host:store.adda247.com" -H "user-agent:Mozilla/5.0 (Linux; Android 11; moto g(40) fusion Build/RRI31.Q1-42-51-8; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/97.0.4692.98 Mobile Safari/537.36" -H "accept:*/*" -H "x-requested-with:com.adda247.app" -H "sec-fetch-site:same-origin" -H "sec-fetch-mode:cors" -H "sec-fetch-dest:empty" -H "referer:https://store.adda247.com/build/pdf.worker.js" -H "accept-encoding:gzip, deflate" -H "accept-language:en-US,en;q=0.9" -H "cookie:cp_token={raw_text5}" "{url}" --output "{name}.pdf"')
                await m.reply_document(f"{name}.pdf", caption=cc)
                count += 1
                await prog.delete(True)
                os.remove(f"{name}.pdf")
                time.sleep(2)
            except Exception as e:
                await m.reply_text(f"{e}\nDownload Failed\n\nName : {name}\n\nLink : {url}")
                continue
    except Exception as e:
        await m.reply_text(e)
    await m.reply_text("Done")


@bot.on_message(filters.command(["jw"]) & (filters.chat(sudo_groups)))
async def account_login(bot: Client, m: Message):
    editable = await m.reply_text("**Hellow deAr,**\n\n**Developer: Smile Bhai**\n**Language:**ðŸ”¥Python\n\n**Send txt file:-**")
    input: Message = await bot.listen(editable.chat.id)
    x = await input.download()
    await input.delete(True)

    path = f"./downloads/{m.chat.id}"

    try:
        with open(x, "r") as f:
            content = f.read()
        content = content.split("\n")
        links = []
        for i in content:
            links.append(i.split(":", 1))
        os.remove(x)
        # print(len(links))
    except:
        await m.reply_text("Invalid file input.ðŸ¥²")
        os.remove(x)
        return

    editable = await m.reply_text(f"Total links found are **{len(links)}**\n\nSend From where you want to download initial is **0**")
    input1: Message = await bot.listen(editable.chat.id)
    raw_text = input1.text

    try:
        arg = int(raw_text)
    except:
        arg = 0

    editable = await m.reply_text("**Enter Title**")
    input0: Message = await bot.listen(editable.chat.id)
    raw_text0 = input0.text

    await m.reply_text("**Enter resolution**")
    input2: Message = await bot.listen(editable.chat.id)
    raw_text2 = input2.text

    editable4 = await m.reply_text("Now send the **Thumb url**\nEg : ```https://telegra.ph/file/1c2a10e73e22774c5ce0e.jpg```\n\nor Send **no**")
    input6 = message = await bot.listen(editable.chat.id)
    raw_text6 = input6.text

    thumb = input6.text
    if thumb.startswith("http://") or thumb.startswith("https://"):
        getstatusoutput(f"wget '{thumb}' -O 'thumb.jpg'")
        thumb = "thumb.jpg"
    else:
        thumb == "no"

    if raw_text == '0':
        count = 1
    else:
        count = int(raw_text)

    try:
        for i in range(arg, len(links)):

            url = links[i][1]
            name1 = links[i][0].replace("\t", "").replace(":", "").replace("/", "").replace("+", "").replace(
                "#", "").replace("|", "").replace("@", "").replace("*", "").replace(".", "").strip()

            if "cpcdn" in url:
                if "playlist" in url:
                    url1 = url.replace("playlist", "360p")
                else:
                    list01 = url.split("/")
                    list01[-1] = "stream_2/stream.m3u8"
                    url1 = "/".join(list01)
            elif "videos" in url:
                list01 = url.replace(".m3u8", "").split("/")
                last01 = list01.pop()
                if len(list01[-1]) > 8:
                    last02 = "video/" + last01 + "-49aced368452fa67022235a5c4b7055c-video-fd.m3u8"
                    list01.append(last02)
                else:
                    last02 = "videos/" + last01 + "-33948335.mp4.m3u8"
                    list01.append(last02)
                url1 = "/".join(list01)

#                 url1 = b
            else:
                url1 = url

            name = f'{str(count).zfill(3)}) {name1}'
            Show = f"**Downloading:-**\n\n**Name :-** `{name}`\n\n**Url :-**\n`{url1}`"
            prog = await m.reply_text(Show)
            cc = f'**Title Â»** {name1}.mkv\n**Caption Â»** {raw_text0}\n**Index Â»** {str(count).zfill(3)}'
            if "pdf" in url:
                cmd = f'yt-dlp -o "{name}.pdf" "{url1}"'
            else:
                cmd = f'yt-dlp --no-check-certificates -o "{name}.mp4" --no-keep-video --remux-video mkv "{url1}"'
            try:
                download_cmd = f"{cmd} -R 25 --fragment-retries 25 --external-downloader aria2c --downloader-args 'aria2c: -x 16 -j 32'"
                os.system(download_cmd)

                if os.path.isfile(f"{name}.mkv"):
                    filename = f"{name}.mkv"
                elif os.path.isfile(f"{name}.mp4"):
                    filename = f"{name}.mp4"
                elif os.path.isfile(f"{name}.pdf"):
                    filename = f"{name}.pdf"
#                 filename = f"{name}.mkv"
                subprocess.run(
                    f'ffmpeg -i "{filename}" -ss 00:01:00 -vframes 1 "{filename}.jpg"', shell=True)
                await prog.delete(True)
                reply = await m.reply_text(f"Uploading - ```{name}```")
                try:
                    if thumb == "no":
                        thumbnail = f"{filename}.jpg"
                    else:
                        thumbnail = thumb
                except Exception as e:
                    await m.reply_text(str(e))

                dur = int(helper.duration(filename))

                start_time = time.time()
                if "pdf" in url1:
                    await m.reply_document(filename, caption=cc)
                else:
                    await m.reply_video(filename, supports_streaming=True, height=720, width=1280, caption=cc, duration=dur, thumb=thumbnail, progress=progress_bar, progress_args=(reply, start_time))
                count += 1
                os.remove(filename)

                os.remove(f"{filename}.jpg")
                await reply.delete(True)
                time.sleep(1)
            except Exception as e:
                await m.reply_text(f"**downloading failed **\n{str(e)}\n**Name** - {name}\n**Link** - `{url}` & `{url1}`")
                continue
    except Exception as e:
        await m.reply_text(e)
    await m.reply_text("Done")

















#   CAREERWILL DOWNLOADER  BOT 













        
         












@bot.on_message(filters.command('pdf'))
async def vision_pdf(bot: Client, m: Message):
    editable = await m.reply_text("**Hello DeAr,** I am Text File Downloader Bot.\nI can download **PDFs of vision** from text file one by one.\n\n**Developer: Smile Bhai** \n**Language:** Python\n**Framework:** 🔥Pyrogram\n\nNow Send Your **TXT File:-**\n")
    input: Message = await bot.listen(editable.chat.id)
    if 2 + 2 == 4: #hehe
        x = await input.download()
        await input.delete(True)

        path = f"./downloads/{m.chat.id}"

        try:
            with open(x, "r") as f:
                content = f.read()
            content = content.split("\n")

            links = []
            for i in content:
                links.append(i.split(":", 1))
            os.remove(x)
        except:
            await m.reply_text("Invalid file input.☹️")
            os.remove(x)
            return
            
    editable = await m.reply_text(f"Total links found are {len(links)}\n\nSend From where you want to download,\n\nInitial is 0")
    input1: Message = await bot.listen(editable.chat.id)
    count = input1.text
    count = int(count)      	
    	            
    await m.reply_text("**Enter Batch Name**")
    inputy: Message = await bot.listen(editable.chat.id)
    raw_texty = inputy.text

    await m.reply_text("**Enter Cookie**")
    input2: Message = await bot.listen(editable.chat.id)
    cookie = input2.text
    cookies = cookies = {'PHPSESSID': f'{cookie}'}
        
    try:
        for i in range(count, len(links)):

            url = links[i][1]
            name1 = links[i][0].replace("\t", "").replace(":", "").replace("/","").replace("+", "").replace("#", "").replace("|", "").replace("@", "").replace("*", "").replace(".", "").strip()[:57]
            name = f'{str(count).zfill(3)}) {name1}'
            cc = f'{str(count).zfill(3)}. {name1}.pdf\n\n**Batch:-** {raw_texty}\n\n'
            ka = await helper.vision(url, name, cookies)
            await m.reply_document(ka, caption=cc)
            count += 1
            os.remove(ka)
            time.sleep(3)
    except Exception as e:
        await m.reply_text(e)
    await m.reply_text("Done.")










#Pwdl





@bot.on_message(filters.command(["pw"]) & (filters.chat(sudo_groups)))
async def txt_handler(bot: Client, m: Message):
    editable  = await m.reply_text("**Hello DeAr,** I am Text File Downloader Bot.\nI can download **Videos of Physics wallah** from text file one by one.\n\n**Developer: Smile Bhai** \n**Language:** Python\n**Framework:** 🔥Pyrogram\n\nNow Send Your **TXT File:-**\n")
    
    input: Message = await bot.listen(editable.chat.id)
    x = await input.download()
     
    path = f"./downloads/{m.chat.id}"

    try:    
     
        with open(x, "r") as f:
             content = f.read()
             content = content.split("\n")
        links = []
        for i in content:
            links.append(i.split("://", 1))
        os.remove(x)
    except Exception as e:
        logging.error(e)
        await m.reply_text("Invalid file input ❌.")
        os.remove(x)
        return

    editable = await m.reply_text(f"Total links found are **{len(links)}**\n\nSend From where you want to download initial is **0**")
    input1: Message = await bot.listen(editable.chat.id)
    raw_text = input1.text


    try:
        arg = int(raw_text)
    except:
        arg = 0
    
    
    editable = await m.reply_text("**Enter Batch Name**")
    input0: Message = await bot.listen(editable.chat.id)
    raw_text0 = input0.text
    
    #editable = await m.reply_text("**Enter Caption**")
#    
#    input7: Message = await bot.listen(editable.chat.id)
#    raw_text7 = input7.text
    
    editable4= await m.reply_text("Now send the **Thumb url**\nEg : ```https://telegra.ph/file/1c2a10e73e22774c5ce0e.jpg```\n\nor Send **no**")
    input6 = message = await bot.listen(editable.chat.id)
    raw_text6 = input6.text

    thumb = input6.text
    if thumb.startswith("http://") or thumb.startswith("https://"):
        getstatusoutput(f"wget '{thumb}' -O 'thumb.jpg'")
        thumb = "thumb.jpg"
    else:
        thumb == "no"

    if raw_text == '0':
        count = 1
    else:
        count = int(raw_text)

    try:
        for i in range(arg, len(links)):
            urlx = "https://" + links[i][1]
            name = links[i][0].replace("\t", "").replace(":", "").replace("/", "").replace("+", "").replace(
                "#", "").replace("|", "").replace("@", "").replace("*", "").replace(".", "").strip()
            url = urlx.replace("d1d34p8vz63oiq", "d26g5bnklkwsh4").replace("mpd", "m3u8").replace("pw2.pc.cdn.bitgravity.com","d26g5bnklkwsh4.cloudfront.net").strip()
            if "zoom" in url:
                cmd = f'yt-dlp "{url}" -o "{name}.%(ext)s"' 
            elif "allen" in url or "vimeo" in url:
                cmd = f'yt-dlp -o "{name}.mp4" -f best --no-keep-video "{url}"'
            elif ".pdf" in url:
                cmd = "pdf"
            elif '.m3u8' in url or 'prourl.xyz' in url:
                cmd = f'yt-dlp "{url}" -o "{name}.%(ext)s"'
            elif 'youtu.be' in url or 'youtube' in url:
                cmd = f'yt-dlp -i -f "bestvideo[height<=480]+bestaudio" --no-keep-video --remux-video mkv --no-warning "{url}" -o "{name}.%(ext)s"'
            else:
                cmd = f'yt-dlp -o "{name}.mp4" -f best --no-keep-video "{url}"'
                


            try:
                Show = f"**Downloading video:-**\n\n**Name :-**\n`{name}\nQuality - Best`\n\n**Url :-**\n`{url}`"
                prog = await m.reply_text(Show)
                cc = f'{str(count).zfill(3)}. {name}.mkv\n**Batch:-** {raw_text0}'
                cc1 =f'{str(count).zfill(3)}. {name}.pdf\n**Batch:-** {raw_text0}\n\n'

                if cmd == "pdf" or ".pdf" in url:
                    try:
                        ka=await helper.aio(url,name)
                        await prog.delete (True)
                        time.sleep(1)
                        reply = await m.reply_text(f"Uploading - ```{name}```")
                        time.sleep(1)
                        start_time = time.time()
                        await m.reply_document(ka, caption=f'**Title »** {name}.pdf\n**Caption »** {raw_text0}\n**Index »** {str(count).zfill(3)}**')
                        count+=1
                        await reply.delete (True)
                        time.sleep(1)
                        os.remove(ka)
                        time.sleep(3)
                    except FloodWait as e:
                        logging.error(e)
                        await m.reply_text(str(e))
                        time.sleep(e.x+1)
                        continue
                else:
                    res_file = await helper.download_video(url,cmd, name)
                    filename = res_file
                    await helper.send_vid(bot, m,cc,filename,thumb,name,prog)
                    count+=1
                    time.sleep(5)
            except Exception as e:
                logging.error(e)
                await m.reply_text(f"**File Not Counted**\n**Name** - {name}\n**Link** - `{url}`")
                time.sleep(30)
                continue


    except Exception as e:
        logging.error(e)
        await m.reply_text(e)
    await m.reply_text("Done.")    






    
@bot.on_message(filters.command(["link"]) & (filters.chat(sudo_groups)))
async def link_handler(bot: Client, m: Message):
    editable = await m.reply_text('Send link in **Name&link** format to download')
    input9: Message = await bot.listen(editable.chat.id)
    raw = input9.text    
    name = raw.split('&')[0]
    url = raw.split('&')[1] or raw
    await m.reply_text("**Enter resolution**")
    input2: Message = await bot.listen(editable.chat.id)
    raw_text2 = input2.text
    
    Show = f"**Downloading Video:-**\n\n**Name :-**\n```{name}\nQuality - {raw_text2}```\n\n**Url :-**\n```{url}```"
    prog = await m.reply_text(Show)
    
    cc = f'{name}'
    
    
    if "youtu" in url:
        if raw_text2 in ["144", "240", "480"]:
            ytf = f'bestvideo[height<={raw_text2}][ext=mp4]+bestaudio[ext=m4a]'
        elif raw_text2 == "360":
            ytf = "18/134"
        elif raw_text2 == "720":
            ytf = "22/136/18"
        elif raw_text2 =="1080":
            ytf = "137/399"
        else:
            ytf = 18
    else:
        ytf=f"bestvideo[height<={raw_text2}]"

    if "jwplayer" in url:
        if raw_text2 in ["180", "144"]:
            try:
                cmd = f'yt-dlp -F "{url}"'
                k = await helper.run(cmd)
                out = helper.vid_info(str(k))
                ytf = f"{out['320x180 ']}/{out['256x144 ']}"
            except Exception as e:
                if e==0:
                    raw_text2=="no"
        elif raw_text2 in ["240", "270"]:
            try:
                cmd = f'yt-dlp -F "{url}"'
                k = await helper.run(cmd)
                out = helper.vid_info(str(k))
                ytf = f"{out['480x270 ']}/{out['426x240 ']}"
            except Exception as e:
                if e==0:
                    raw_text2=="no"
        elif raw_text2 == "360":
            try:
                cmd = f'yt-dlp -F "{url}"'
                k = await helper.run(cmd)
                out = helper.vid_info(str(k))
                ytf = out['640x360 ']
            except Exception as e:
                if e == 0:
                    raw_text2=="no"
        elif raw_text2 == "480":
            try:
                cmd = f'yt-dlp -F "{url}"'
                k = await helper.run(cmd)
                out = helper.vid_info(str(k))
                ytf = f"{out['960x540 ']}/{out['852x480 ']}"
            except Exception as e:
                if e==0:
                    raw_text2=="no"
        elif raw_text2 == "720":
            try:
                cmd = f'yt-dlp -F "{url}"'
                k = await helper.run(cmd)
                out = helper.vid_info(str(k))
                ytf = f"{out['1280x720 ']}"
            except Exception as e:
                if e==0:
                    raw_text2=="no"
        elif raw_text2 == "1080":
            try:
                cmd = f'yt-dlp -F "{url}"'
                k = await helper.run(cmd)
                out = helper.vid_info(str(k))
                ytf =f"{out['1920x1080 ']}/{['1920x1056']}"
            except Exception as e:
                if e==0:
                    raw_text2=="no"
        else:
            raw_text2=="no"

    if ytf == f'bestvideo[height<={raw_text2}][ext=mp4]+bestaudio[ext=m4a]':
        cmd = f'yt-dlp -o "{name}.mp4" -f "{ytf}" "{url}"'

    elif "adda247" in url:
        cmd=f'yt-dlp -o "{name}.mp4" "{url}"'
    elif "kdcampus" or "streamlock" in url:
        cmd=f'yt-dlp -o "{name}.mp4" "{url}"'
    elif ".pdf" in url:
        cmd = f'yt-dlp -o "{name}.pdf" "{url}"'
    elif "drive" in url:
        cmd = f'yt-dlp -o "{name}.pdf" "{url}"'
    elif raw_text2 == "no":
        cmd=f'yt-dlp -o "{name}.mp4" "{url}"'
    else:
        cmd = f'yt-dlp -o "{name}.mp4" -f "{ytf}+bestaudio" "{url}"'

    try:
        download_cmd = f"{cmd} -R 25 --fragment-retries 25 --external-downloader aria2c --downloader-args 'aria2c: -x 16 -j 32'"
        os.system(download_cmd)
        filename = f"{name}.mp4"
        subprocess.run(f'ffmpeg -i "{filename}" -ss 00:01:00 -vframes 1 "{filename}.jpg"', shell=True)
        thumbnail = f"{filename}.jpg"
        dur = int(helper.duration(filename))
        await prog.delete (True)
        try:
            await m.reply_video(f"{name}.mp4",caption=cc, supports_streaming=True,height=720,width=1280,thumb=thumbnail,duration=dur)
        except:
            await m.reply_text("There was an error while uploading file as streamable so, now trying to upload as document.")
            await m.reply_document(f"{name}.webm",caption=cc)
        os.remove(f"{name}.mp4")
        os.remove(f"{filename}.jpg")
    except Exception as e:
        await m.reply_text(e)





        
@bot.on_message(filters.command(["url"]) & (filters.chat(sudo_groups)))
async def ytdlp_handler(bot: Client, m: Message):
    editable = await m.reply_text('Send link in **Name&link** format to get its info')
    input: Message = await bot.listen(editable.chat.id)
    raw_file = input.text    
    name = raw_file.split('&')[0]
    url = raw_file.split('&')[1] 
    cmd = f'yt-dlp -F "{url}"'
    k = await helper.run(cmd)
    out = helper.parse_vid_info(str(k))
    await m.reply_text(out)
    buttons = []
    if 'unknown' in out[0][1]:
        r = await m.reply_text("Its Unknown so Downloading...")
        f = helper.old_download(url, name)
        await m.reply_document(
        document=f,caption=name
        )
        await r.delete(True)
        return
    
    for i in out:
        if 'youtu' in url:
            await m.reply_text(i[1])
            x = i[1].split()[0].split("x")[-1]
            buttons.append(InlineKeyboardButton(i[1], callback_data=f"id:bestvideo[height<={x}][ext=mp4]"))
        else:
            buttons.append(InlineKeyboardButton(i[1], callback_data=f"id:{i[0]}"))
    buttons_markup = InlineKeyboardMarkup([buttons])
    await m.reply(f"Name : `{name}`\n\n:Link : `{url}`",reply_markup=buttons_markup)





bot.run()






    


