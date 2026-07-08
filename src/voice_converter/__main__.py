import logging

from telegram.ext import ApplicationBuilder, MessageHandler, filters

from .config import BOT_TOKEN
from .handlers import convert_media_to_voice


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)


def main() -> None:
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(
        MessageHandler(
            filters.AUDIO | filters.VIDEO | filters.VOICE, convert_media_to_voice
        )
    )

    app.run_polling()


if __name__ == "__main__":
    main()
