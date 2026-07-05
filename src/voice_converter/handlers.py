from telegram import Update
from telegram.ext import ContextTypes


async def hello(update: Update, contex: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f"Hello {update.effective_user.first_name}")


async def handle_media(update: Update, contex: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.message
    media = message.audio or message.video or message.voice
    telegram_file = await media.get_file()
    file_bytes = await telegram_file.download_as_bytearray()
    await update.message.reply_voice(voice=file_bytes, reply_to_message_id=message.id)