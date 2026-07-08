import logging

from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

from .config import BOT_TOKEN
from .handlers import start, convert_media_to_voice


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)


def main() -> None:
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    media_filter = filters.AUDIO | filters.VIDEO | filters.VOICE
    app.add_handler(MessageHandler(media_filter, convert_media_to_voice))

    app.run_polling()


if __name__ == "__main__":
    main()
