from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

from .config import BOT_TOKEN

import subprocess
import tempfile
import os

MAX_FILE_SIZE = 20 * 1024 * 1024  # 20 MB


def opus_encode(file_bytes: bytes, voice_filter: str | None) -> bytes:
    with tempfile.NamedTemporaryFile(delete=False) as fp:
        fp.write(file_bytes)
        input_file = fp.name

    with tempfile.NamedTemporaryFile(delete=False, suffix=".ogg") as fp:
        output_file = fp.name

    command = ["ffmpeg", "-i", input_file, "-vn"]
    if voice_filter:
        command.extend(["-filter:a", voice_filter])
    command.extend(["-codec:a", "libopus", output_file, "-y"])
    subprocess.run(command)

    with open(output_file, "rb") as f:
        opus_bytes = f.read()

    os.unlink(input_file)
    os.unlink(output_file)

    return opus_bytes


async def hello(update: Update, contex: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f"Hello {update.effective_user.first_name}")


def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("hello", hello))

    app.run_polling()


if __name__ == "__main__":
    main()
