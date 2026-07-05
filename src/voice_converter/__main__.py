import logging

from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

from .config import BOT_TOKEN
from .handlers import hello, handle_media

import subprocess
import tempfile
import os


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)


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


def main() -> None:
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("hello", hello))
    app.add_handler(
        MessageHandler(filters.AUDIO | filters.VIDEO | filters.VOICE, handle_media)
    )

    app.run_polling()


if __name__ == "__main__":
    main()
