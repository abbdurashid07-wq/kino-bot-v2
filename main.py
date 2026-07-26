from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

from config import TOKEN
from database import get_movie, add_movie

ADMIN_ID = 8885454283

waiting_video = {}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎬 Assalomu alaykum!\n\nKino kodini yuboring."
    )


async def admin_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    waiting_video[ADMIN_ID] = update.message.video.file_id

    await update.message.reply_text(
        "✅ Endi kino kodini yuboring."
    )


async def movie(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    if update.effective_user.id == ADMIN_ID and ADMIN_ID in waiting_video:
        add_movie(text, waiting_video[ADMIN_ID])
        del waiting_video[ADMIN_ID]
        await update.message.reply_text("✅ Kino saqlandi.")
        return

    file_id = get_movie(text)

    if file_id:
        await update.message.reply_video(file_id)
    else:
        await update.message.reply_text("❌ Bunday kod topilmadi.")


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.VIDEO, admin_video))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, movie))

    print("Bot ishga tushdi...")
    app.run_polling()


if __name__ == "__main__":
    main()
