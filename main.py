from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)

from config import TOKEN
from database import get_movie, add_movie

ADMIN_ID = 8885454283
CHANNEL = "@Marvel_kino_kod"

waiting_video = {}


async def check_sub(user_id, context):
    member = await context.bot.get_chat_member(CHANNEL, user_id)
    return member.status in ["member", "administrator", "creator"]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_sub(update.effective_user.id, context):
        keyboard = [
            [InlineKeyboardButton("📢 Kanalga qo'shilish", url="https://t.me/Marvel_kino_kod")],
            [InlineKeyboardButton("✅ Tekshirish", callback_data="check")]
        ]

        await update.message.reply_text(
            "❌ Botdan foydalanish uchun avval kanalga a'zo bo'ling.",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )
        return

    await update.message.reply_text(
        "🎬 Assalomu alaykum!\n\nKino kodini yuboring."
    )


async def check_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if await check_sub(query.from_user.id, context):
        await query.message.edit_text(
            "✅ Rahmat! Endi botdan foydalanishingiz mumkin.\n\n/start ni bosing."
        )
    else:
        await query.answer(
            "❌ Siz hali kanalga a'zo emassiz!",
            show_alert=True,
        )


async def admin_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    waiting_video[ADMIN_ID] = update.message.video.file_id

    await update.message.reply_text(
        "✅ Endi kino kodini yuboring."
    )


async def movie(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_sub(update.effective_user.id, context):
        keyboard = [
            [InlineKeyboardButton("📢 Kanalga qo'shilish", url="https://t.me/Marvel_kino_kod")],
            [InlineKeyboardButton("✅ Tekshirish", callback_data="check")]
        ]

        await update.message.reply_text(
            "❌ Avval kanalga a'zo bo'ling.",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )
        return

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
    app.add_handler(CallbackQueryHandler(check_button))
    app.add_handler(MessageHandler(filters.VIDEO, admin_video))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, movie))

    print("Bot ishga tushdi...")
    app.run_polling()


if __name__ == "__main__":
    main()
