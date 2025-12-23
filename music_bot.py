from pyrogram import Client, filters
from pytgcalls import PyTgCalls
from pytgcalls.types.input_stream import AudioPiped
import yt_dlp
import os

from config import API_ID, API_HASH, BOT_TOKEN

app = Client(
    "musicbot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

call = PyTgCalls(app)

def yt_download(query):
    ydl_opts = {
        "format": "bestaudio",
        "outtmpl": "song.mp3",
        "quiet": True
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.extract_info(f"ytsearch1:{query}", download=True)

@app.on_message(filters.command("play") & filters.group)
async def play(_, msg):
    if len(msg.command) < 2:
        await msg.reply("song name do")
        return

    query = " ".join(msg.command[1:])
    await msg.reply("downloading from YouTube...")

    yt_download(query)

    await call.join_group_call(
        msg.chat.id,
        AudioPiped("song.mp3"),
    )

    await msg.reply(f"▶️ Playing: {query}")

@app.on_message(filters.command("stop"))
async def stop(_, msg):
    await call.leave_group_call(msg.chat.id)
    await msg.reply("⏹ stopped")

app.start()
call.start()
print("YT Music Bot Running...")
app.idle()