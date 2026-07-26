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
from database import (
    get_movie,
    add_movie,
    add_user,
    user_count,
    get_users,
    delete_movie,
)

ADMIN_ID = 8885454283
CHANNEL = "@Marvel_kino_kod"

waiting_video = {}


async def check_sub(user_id, context):
    member = await context.bot.get_chat_member(CHANNEL, user_id)
    return member.status in ["member", "administrator", "creator"]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    add_user(update.effective_user.id)

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

    if not update.message.video:
        return

    waiting_video[ADMIN_ID] = update.message.video.file_id

    await update.message.reply_text(
        "✅ Endi kino kodini yuboring."
    )


async def movie(update: Update, context: ContextTypes.DEFAULT_TYPE):
    add_user(update.effective_user.id)

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
      
async def stat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    await update.message.reply_text(
        f"👥 Foydalanuvchilar soni: {user_count()} ta"
    )
async def delete(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    if len(context.args) != 1:
        await update.message.reply_text(
            "❗ Foydalanish:\n/delete 101"
        )
        return

    code = context.args[0]
    delete_movie(code)

    await update.message.reply_text(
        f"🗑 {code} kodli kino o'chirildi."
    )


async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    if not context.args:
        await update.message.reply_text(
            "❗ Foydalanish:\n/broadcast Salom hammaga!"
        )
        return

    text = " ".join(context.args)

    sent = 0

    for user_id in get_users():
        try:
            await context.bot.send_message(chat_id=user_id, text=text)
            sent += 1
        except Exception:
            pass

    await update.message.reply_text(
        f"✅ Xabar {sent} ta foydalanuvchiga yuborildi."
    )


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stat", stat))
    app.add_handler(CommandHandler("delete", delete))
    app.add_handler(CommandHandler("broadcast", broadcast))

    app.add_handler(CallbackQueryHandler(check_button))
    app.add_handler(MessageHandler(filters.VIDEO, admin_video))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, movie))

    print("Bot ishga tushdi...")
    app.run_polling()

if __name__ == "__main__":
    main()
