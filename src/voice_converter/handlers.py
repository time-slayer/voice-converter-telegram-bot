import asyncio
import tempfile
import os

from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ChatAction



async def convert_media_to_voice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_chat_action(ChatAction.UPLOAD_VOICE)

    message = update.message
    media = message.audio or message.video or message.voice
    if not media:
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
                await update.message.reply_voice(
                    voice=f, reply_to_message_id=message.id
                )
        else:
            await update.message.reply_text("Failed to convert")
