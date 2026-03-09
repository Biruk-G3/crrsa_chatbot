from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import os
from bot.ai import ask_ai  # your AI function

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

# store user language
user_languages = {}

# language selection buttons
LANG_BUTTONS = [["English", "አማርኛ", "Afaan Oromo"]]

# service names translations
SERVICE_NAMES = {
    "en": ["Resident Registration", "Birth Certificate", "Marriage Certificate", "Divorce Certificate", "Death Certificate"],
    "am": ["የነዋሪ ምዝገባ", "የልደት ሰርተፍኬት", "የጋብቻ ሰርተፍኬት", "የፍቺ ሰርተፍኬት", "የሞት ሰርተፍኬት"],
    "or": ["Galmee Jiraataa", "Ragaa Dhalootaa", "Ragaa Gaa'elaa", "Ragaa Hiikkaa Gaa'elaa", "Ragaa Du'aa"]
}

# service descriptions (for button replies)
SERVICE_DESCRIPTIONS = {
    "en": {
        "Resident Registration": "We register residents and provide them an ID card. Must live in the woreda.",
        "Birth Certificate": "We issue birth certificates to residents. Must have woreda ID card.",
        "Marriage Certificate": "We provide marriage certificates. At least one must be a resident.",
        "Divorce Certificate": "We provide divorce certificates following legal procedures.",
        "Death Certificate": "We provide death certificates for residents who have passed away in this woreda."
    },
    "am": {
        "የነዋሪ ምዝገባ": "ነዋሪዎችን እና መታወቂያ ካርድ ለመስጠት እንመዝግባለን። በወረዳ ውስጥ መኖር አለበት።",
        "የልደት ሰርተፍኬት": "ለነዋሪዎች የልደት ሰርተፍኬት እንሰጣለን። የወረዳ መታወቂያ ካርድ አለበት።",
        "የጋብቻ ሰርተፍኬት": "የጋብቻ ሰርተፍኬት እንሰጣለን። ቢያንስ አንዱ ነዋሪ መሆን አለበት።",
        "የፍቺ ሰርተፍኬት": "የፍቺ ሰርተፍኬት በሕጋዊ ሂደት እንሰጣለን።",
        "የሞት ሰርተፍኬት": "ለነዋሪዎች የሞት ሰርተፍኬት እንሰጣለን።"
    },
    "or": {
        "Galmee Jiraataa": "Jiraatota galmeessina kaardii eenyummaa ni kennina. Jiraataa ta'uu qaba.",
        "Ragaa Dhalootaa": "Ragaa dhalootaa ni kennaaf jiraatotaaf. Kaardii eenyummaa qabaachuu qaba.",
        "Ragaa Gaa'elaa": "Ragaa gaa'elaa ni kennaaf. Tokkichi jiraataa ta'uu qaba.",
        "Ragaa Hiikkaa Gaa'elaa": "Ragaa hiikkaa gaa'elaa seera qabeessa ta'een ni kenna.",
        "Ragaa Du'aa": "Ragaa du'aa ni kennaaf jiraatota du'an."
    }
}

def detect_language(text):
    if text == "English":
        return "en"
    if text == "አማርኛ":
        return "am"
    if text == "Afaan Oromo":
        return "or"
    return None

def build_service_keyboard(lang):
    names = SERVICE_NAMES[lang]
    keyboard = [
        names[0:2],  # row 1
        names[2:4],  # row 2
        [names[4]]   # row 3
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = ReplyKeyboardMarkup(LANG_BUTTONS, resize_keyboard=True)
    await update.message.reply_text(
        "Welcome to the Civil Registration Service Bot.\nPlease choose your language.",
        reply_markup=keyboard
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    text = update.message.text

    # Check if user is selecting a language
    lang = detect_language(text)
    if lang:
        user_languages[user_id] = lang
        service_keyboard = build_service_keyboard(lang)
        messages = {
            "en": "Language set to English. Please choose a service or ask a question.",
            "am": "ቋንቋ አማርኛ ተመርጧል። እባክዎ አገልግሎት ይምረጡ ወይም ጥያቄዎን ይጠይቁ።",
            "or": "Afaan filatameera. Tajaajila filadhu yookiin gaaffii kee gaafadhu."
        }
        await update.message.reply_text(messages[lang], reply_markup=service_keyboard)
        return

    # Get user’s language, default to English
    lang = user_languages.get(user_id, "en")

    # Check if the message matches a service button
    if text in SERVICE_NAMES[lang]:
        description = SERVICE_DESCRIPTIONS[lang].get(text)
        if description:
            await update.message.reply_text(description)
            return

    # Otherwise, send message to AI
    answer = ask_ai(text, lang)
    await update.message.reply_text(answer)

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Bot is running...")
    app.run_polling()
