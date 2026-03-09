from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import os
from bot.ai import ask_ai  # make sure your ai.py accepts lang parameter

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

# store user language
user_languages = {}

# language buttons
LANG_BUTTONS = [["English", "አማርኛ", "Afaan Oromo"]]
keyboard = ReplyKeyboardMarkup(LANG_BUTTONS, resize_keyboard=True, one_time_keyboard=True)

# ----------------- Start command -----------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Welcome to the Civil Registration Service Bot.\nPlease choose your language.",
        reply_markup=keyboard
    )

# ----------------- Detect language -----------------
def detect_language(text):
    if text == "English":
        return "en"
    if text == "አማርኛ":
        return "am"
    if text == "Afaan Oromo":
        return "or"
    return None

# ----------------- Handle messages -----------------
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    text = update.message.text

    # check if user is selecting language
    lang = detect_language(text)
    if lang:
        user_languages[user_id] = lang
        remove_keyboard = ReplyKeyboardRemove()

        if lang == "en":
            await update.message.reply_text("Language set to English. Ask your question.", reply_markup=remove_keyboard)
        elif lang == "am":
            await update.message.reply_text("ቋንቋ አማርኛ ተመርጧል። ጥያቄዎን ይጠይቁ።", reply_markup=remove_keyboard)
        elif lang == "or":
            await update.message.reply_text("Afaan filatameera. Gaaffii kee gaafadhu.", reply_markup=remove_keyboard)

        return

    # get saved language, default to English
    lang = user_languages.get(user_id, "en")

    # send question to AI with language
    answer = ask_ai(text, lang)

    await update.message.reply_text(answer)

# ----------------- Main bot -----------------
if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()

    # Handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot is running...")
    app.run_polling()
