from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

BOT_TOKEN = "8134187462:AAHlwuANjWdEFbraKjuKh-vSCYMbuWt92ow"

user_addresses = {}

# دکمه‌ها
def main_keyboard():
    keyboard = [
        [InlineKeyboardButton("📄 اطلاعات توکن", callback_data="token"),
         InlineKeyboardButton("💧 استخر نقدینگی", callback_data="pool")],
        [InlineKeyboardButton("🎁 ایردراپ", callback_data="airdrop"),
         InlineKeyboardButton("📌 سوالات پرتکرار", callback_data="faq")],
        [InlineKeyboardButton("📬 تماس با ادمین", callback_data="contact")]
    ]
    return InlineKeyboardMarkup(keyboard)

# start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🌟 خوش اومدی به ربات رسمی توکن HAKHAMEN (HKM)\n\n👇 انتخاب کن:",
        reply_markup=main_keyboard()
    )

# مدیریت کلیک‌ها
async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "token":
        await query.edit_message_text(
            "🪙 اطلاعات توکن HKM:\n"
            "نام: HAKHAMEN\n"
            "نماد: HKM\n"
            "Decimals: 6\n"
            "Total Supply: 100,000,000\n"
            "آدرس قرارداد:\n"
            "`EQC_tZ2xxrbjWptQrtlbAV5GWnLdnUG-T4UQECIT7YxWrwmw`",
            parse_mode='Markdown'
        )

    elif query.data == "pool":
        await query.edit_message_text(
            "🔗 استخر نقدینگی:\n"
            "https://app.ston.fi/swap?chartVisible=false&ft=TON&tt=EQC_tZ2xxrbjWptQrtlbAV5GWnLdnUG-T4UQECIT7YxWrwmw"
        )

    elif query.data == "faq":
        await query.edit_message_text(
            "📌 سوالات پرتکرار:\n"
            "– HKM رو از کجا بخرم؟\n"
            "👉 از استخر Ston: /pool\n"
            "– کیف پول مناسب چیه؟\n"
            "👉 TON Keeper یا MyTonWallet\n"
            "– چجوری نقدینگی بدم؟\n"
            "👉 آموزش در وب‌سایت رسمی به‌زودی"
        )

    elif query.data == "contact":
        await query.edit_message_text("📬 تماس با ادمین: @hakhmen")

    elif query.data == "airdrop":
        await query.edit_message_text("🔐 لطفاً آدرس کیف پول TON خودتو بفرست تا ذخیره بشه:")
        context.user_data["awaiting_wallet"] = True

# ذخیره آدرس TON
async def save_wallet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if context.user_data.get("awaiting_wallet"):
        user_addresses[user_id] = update.message.text
        context.user_data["awaiting_wallet"] = False
        await update.message.reply_text("✅ آدرس ذخیره شد. مرسی رفیق!")
    else:
        await update.message.reply_text("❗ لطفاً از دکمه‌ها استفاده کن.")

# راه‌اندازی ربات
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_buttons))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, save_wallet))

    app.run_polling()

if name == '__main__':
    main()
