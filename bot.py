import google.generativeai as genai
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import os

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-3.1-flash-lite")

SYSTEM_PROMPT = """Tu ek ekdum mast roasting AI hai Mumbai ka!
Tu users ki zabardast funny roasting karta hai - bilkul dost ki tarah.
Mumbai slang use kar - bantai, aiba, abe, bhai, yaar, scene etc.
Roast funny honi chahiye, dil se nahi lagni chahiye.
Har roast ke baad "Par tu mera bantai hai!" type ending rakh.
Hindi + English mix mein baat kar."""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Aiba bantai! 🔥\nKya scene hai?\nAa teri roasting karta hoon - bol apne baare mein kuch! 😂"
    )

async def roast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    await update.message.reply_text("Ruk bantai, soch raha hoon teri... 🤔")
    try:
        full_prompt = f"{SYSTEM_PROMPT}\n\nUser ne yeh bola: {user_message}\n\nAb iska zabardast funny roast kar!"
        response = model.generate_content(full_prompt)
        await update.message.reply_text(response.text)
    except Exception as e:
        await update.message.reply_text(f"Aiba lafda: {str(e)}")

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, roast))
    print("Roasting bot chal raha hai!")
    app.run_polling()

if __name__ == "__main__":
    main()
