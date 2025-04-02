import os
import re
import sys
import time
import logging
import requests
import subprocess
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import FloodWait
from pyromod import listen
import tgcrypto
from urllib.parse import parse_qs, urlparse
from subprocess import getstatusoutput
import helper
import aiohttp
import asyncio
import aiofiles
from aiohttp import ClientSession
from pyrogram.types import InputMediaDocument
from psutil import disk_usage, cpu_percent, swap_memory, cpu_count, virtual_memory, net_io_counters, boot_time
import yt_dlp

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    stream=sys.stdout
)

# Environment variables (for Koyeb)
API_ID = int(os.environ.get("API_ID", "28017074"))
API_HASH = os.environ.get("API_HASH", "d1992b608fb66ffbaf9e8e441a562bc5")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "6462557323:AAGhmSMvcrvxHo6IIev9D6COwitGZ6WGvsM")
SUDO_GROUPS = list(map(int, os.environ.get("SUDO_GROUPS", "-1002467329974").split()))

# Global variables
botStartTime = time.time()
batch = []

# Initialize Pyrogram Client
bot = Client(
    "ntxt_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# Utility Functions
def meFormatter(milliseconds: int) -> str:
    """Format time in human readable format"""
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    return f"{days}d, {hours}h, {minutes}m, {seconds}s" if days else f"{hours}h, {minutes}m, {seconds}s"

def humanbytes(size: int) -> str:
    """Convert bytes to human readable format"""
    power = 2**10
    n = 0
    units = {0: 'B', 1: 'KB', 2: 'MB', 3: 'GB', 4: 'TB'}
    while size > power and n < 4:
        size /= power
        n += 1
    return f"{size:.2f} {units[n]}"

async def is_admin(chat_id: int, user_id: int) -> bool:
    """Check if user is admin in sudo groups"""
    try:
        for group in SUDO_GROUPS:
            members = await bot.get_chat_members(group)
            if any(member.user.id == user_id for member in members):
                return True
    except Exception:
        pass
    return False

# Command Handlers
@bot.on_message(filters.command(["start"]) & filters.chat(SUDO_GROUPS))
async def start_handler(_, message: Message):
    """Handle /start command"""
    menu = (
        "🚀 **Ntxt Downloader Bot**\n\n"
        "**Available Commands:**\n"
        "/pdf - Download PDFs from links\n"
        "/txt - Download videos from text file\n"
        "/zip - Process zip files\n"
        "/stats - Show bot statistics\n"
        "/restart - Restart the bot\n\n"
        "**Admin Only**"
    )
    await message.reply_text(menu)

@bot.on_message(filters.command(["restart"]))
async def restart_handler(_, message: Message):
    """Restart the bot"""
    if not await is_admin(message.chat.id, message.from_user.id):
        return await message.reply_text("⚠️ Admin access required!")
    
    await message.reply_text("🔄 Restarting bot...")
    os.execl(sys.executable, sys.executable, *sys.argv)

@bot.on_message(filters.command(["stats"]))
async def stats_handler(_, message: Message):
    """Show system statistics"""
    currentTime = meFormatter(time.time() - botStartTime)
    osUptime = meFormatter(time.time() - boot_time())
    
    disk = disk_usage('/')
    net = net_io_counters()
    swap = swap_memory()
    memory = virtual_memory()
    
    stats = (
        f"⏱ **Bot Uptime:** {currentTime}\n"
        f"🖥 **OS Uptime:** {osUptime}\n\n"
        f"💾 **Disk:** {humanbytes(disk.used)} / {humanbytes(disk.total)} ({disk.percent}%)\n"
        f"📊 **RAM:** {humanbytes(memory.used)} / {humanbytes(memory.total)} ({memory.percent}%)\n"
        f"🔁 **Swap:** {humanbytes(swap.used)} / {humanbytes(swap.total)} ({swap.percent}%)\n\n"
        f"⬆️ **Upload:** {humanbytes(net.bytes_sent)}\n"
        f"⬇️ **Download:** {humanbytes(net.bytes_recv)}\n\n"
        f"🖥 **CPU:** {cpu_percent()}%\n"
        f"🧵 **Cores:** {cpu_count(logical=False)}P + {cpu_count(logical=True)-cpu_count(logical=False)}L"
    )
    
    await message.reply_text(stats)

@bot.on_message(filters.command(["pdf"]) & filters.chat(SUDO_GROUPS))
async def pdf_handler(_, message: Message):
    """Handle PDF downloads"""
    if not await is_admin(message.chat.id, message.from_user.id):
        return await message.reply_text("⚠️ Admin access required!")
    
    editable = await message.reply_text("📄 Send TXT file with PDF links (format: Name:URL)")
    input_msg = await bot.listen(message.chat.id, timeout=300)
    
    try:
        file_path = await input_msg.download()
        with open(file_path, "r") as f:
            links = [line.strip().split(":", 1) for line in f if line.strip()]
        
        if not links:
            return await message.reply_text("❌ No valid links found")
        
        await editable.edit(f"📚 Found {len(links)} PDF links\nEnter starting index (default: 1):")
        input_start = await bot.listen(message.chat.id, timeout=60)
        start_from = int(input_start.text) if input_start.text.isdigit() else 1
        
        await editable.edit("📛 Enter batch name:")
        input_batch = await bot.listen(message.chat.id, timeout=60)
        batch_name = input_batch.text
        
        success = 0
        for i in range(start_from-1, len(links)):
            name, url = links[i]
            try:
                response = requests.get(url, stream=True)
                if response.status_code == 200:
                    with open(f"{name}.pdf", 'wb') as f:
                        for chunk in response.iter_content(1024):
                            f.write(chunk)
                    
                    caption = f"📄 {name}.pdf\n\nBatch: {batch_name}"
                    await message.reply_document(
                        document=f"{name}.pdf",
                        caption=caption
                    )
                    os.remove(f"{name}.pdf")
                    success += 1
                    time.sleep(2)
            except Exception as e:
                logging.error(f"Error downloading {url}: {e}")
        
        await message.reply_text(f"✅ Completed! Successfully downloaded {success}/{len(links)} PDFs")
    
    except Exception as e:
        await message.reply_text(f"❌ Error: {str(e)}")
    finally:
        if 'file_path' in locals() and os.path.exists(file_path):
            os.remove(file_path)

@bot.on_message(filters.command(["txt"]) & filters.chat(SUDO_GROUPS))
async def txt_handler(_, message: Message):
    """Handle video downloads from txt"""
    if not await is_admin(message.chat.id, message.from_user.id):
        return await message.reply_text("⚠️ Admin access required!")
    
    editable = await message.reply_text("📄 Send TXT file with video links (format: Name:URL)")
    input_msg = await bot.listen(message.chat.id, timeout=300)
    
    try:
        file_path = await input_msg.download()
        with open(file_path, "r") as f:
            links = [line.strip().split(":", 1) for line in f if line.strip()]
        
        if not links:
            return await message.reply_text("❌ No valid links found")
        
        await editable.edit(f"🎬 Found {len(links)} video links\nEnter starting index (default: 1):")
        input_start = await bot.listen(message.chat.id, timeout=60)
        start_from = int(input_start.text) if input_start.text.isdigit() else 1
        
        await editable.edit("📛 Enter batch name:")
        input_batch = await bot.listen(message.chat.id, timeout=60)
        batch_name = input_batch.text
        
        await editable.edit("🖼 Enter resolution (144,240,360,480,720,1080):")
        input_res = await bot.listen(message.chat.id, timeout=60)
        resolution = input_res.text
        
        await editable.edit("📝 Enter caption or /skip:")
        input_caption = await bot.listen(message.chat.id, timeout=60)
        caption = "" if input_caption.text == "/skip" else input_caption.text
        
        await editable.edit("🖼 Send thumbnail URL or /skip:")
        input_thumb = await bot.listen(message.chat.id, timeout=60)
        thumb_url = None if input_thumb.text == "/skip" else input_thumb.text
        
        # Download thumbnail if provided
        thumb_path = None
        if thumb_url and thumb_url.startswith(("http://", "https://")):
            thumb_path = "thumbnail.jpg"
            os.system(f"wget '{thumb_url}' -O {thumb_path}")
        
        # Process links
        success = 0
        for i in range(start_from-1, len(links)):
            name, url = links[i]
            try:
                ydl_opts = {
                    'format': f'bestvideo[height<={resolution}]+bestaudio/best[height<={resolution}]',
                    'outtmpl': f'{name}.%(ext)s',
                    'quiet': True
                }
                
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    filename = ydl.prepare_filename(info)
                
                post_caption = f"🎬 {name}\n\nBatch: {batch_name}\n\n{caption}" if caption else f"🎬 {name}\n\nBatch: {batch_name}"
                
                await message.reply_video(
                    video=filename,
                    caption=post_caption,
                    thumb=thumb_path,
                    supports_streaming=True
                )
                os.remove(filename)
                success += 1
                time.sleep(5)
            except Exception as e:
                logging.error(f"Error downloading {url}: {e}")
        
        await message.reply_text(f"✅ Completed! Successfully downloaded {success}/{len(links)} videos")
    
    except Exception as e:
        await message.reply_text(f"❌ Error: {str(e)}")
    finally:
        if 'file_path' in locals() and os.path.exists(file_path):
            os.remove(file_path)
        if thumb_path and os.path.exists(thumb_path):
            os.remove(thumb_path)


    bot.run()
