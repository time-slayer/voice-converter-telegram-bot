import asyncio
import os
import tempfile

from telegram import Update
from telegram.constants import ChatAction, FileSizeLimit
from telegram.ext import ContextTypes


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_name = update.effective_user.first_name
    start_message = (
        f"Hi, {user_name}\n"
        "I can convert media into a voice message\n"
        "You can send me one or more media files at once"
    )
    await update.message.reply_text(start_message)


async def convert_media_to_voice(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    await update.message.reply_chat_action(ChatAction.RECORD_VOICE)

    message = update.message
    media = message.audio or message.video or message.voice
    if not media:
        return

    if media.file_size and media.file_size > FileSizeLimit.FILESIZE_DOWNLOAD:
        await message.reply_text(
            f"Media file is too large to download. Current limit is 20 MB",
            do_quote=True,
        )
        return

    telegram_file = await media.get_file()

    with tempfile.TemporaryDirectory() as tmp_dir:
        input_path = os.path.join(tmp_dir, "input")
        output_path = os.path.join(tmp_dir, "output.ogg")

        await telegram_file.download_to_drive(input_path)

        process = await asyncio.create_subprocess_exec(
            "ffmpeg",
            "-i",
            input_path,
            "-vn",
            "-c:a",
            "libopus",
            output_path,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        await process.communicate()

        if process.returncode == 0:
            with open(output_path, "rb") as f:
                await update.message.reply_voice(voice=f, do_quote=True)
        else:
            await update.message.reply_text("Failed to convert", do_quote=True)
