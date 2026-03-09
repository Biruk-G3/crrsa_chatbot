from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import os
from bot.ai import ask_ai

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

# store user language
user_languages = {}

# language buttons
LANG_BUTTONS = [["English", "አማርኛ", "Afaan Oromo"]]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = ReplyKeyboardMarkup(LANG_BUTTONS, resize_keyboard=True)

    await update.message.reply_text(
        "Welcome to the Civil Registration Service Bot.\nPlease choose your language.",
        reply_markup=keyboard
    )


def detect_language(text):

    if text == "English":
        return "en"

    if text == "አማርኛ":
        return "am"

    if text == "Afaan Oromo":
        return "or"

    return None


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.message.from_user.id
    text = update.message.text

    lang = detect_language(text)

    # user selecting language
    if lang:

        user_languages[user_id] = lang

        if lang == "en":
            await update.message.reply_text("Language set to English. Ask your question.")

        elif lang == "am":
            await update.message.reply_text("ቋንቋ አማርኛ ተመርጧል። ጥያቄዎን ይጠይቁ።")

        elif lang == "or":
            await update.message.reply_text("Afaan filatameera. Gaaffii kee gaafadhu.")

        return

    # get saved language
    lang = user_languages.get(user_id, "en")

    # send question to AI with language
    answer = ask_ai(text, lang)

    await update.message.reply_text(answer)


if __name__ == "__main__":

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot is running...")

    app.run_polling()
