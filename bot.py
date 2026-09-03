import google.generativeai as genai
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import os

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-3.1-flash-lite")

SYSTEM_PROMPT = """Tu ek Mumbai ka bindaas AI hai. 
Tu hamesha Mumbai street slang mein baat karta hai.
Jaise: bhai, yaar, abe, aiba, bantai, ekdum fatafat, mast, bindaas, 
solid, jhakkas, lafda, chakkar, scene, jugaad etc.
Short aur mast jawab de. Gyaan zyada mat jhaad."""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Aiba! Kya scene hai bantai! 🤙\nMain DinoAI hoon - bol kya chahiye!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    await update.message.reply_text("Soch raha hoon bantai... 🤔")
    try:
        full_prompt = f"{SYSTEM_PROMPT}\n\nUser: {user_message}"
        response = model.generate_content(full_prompt)
        await update.message.reply_text(response.text)
    except Exception as e:
        await update.message.reply_text(f"Aiba lafda ho gaya: {str(e)}")

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("DinoAI chal raha hai!")
    app.run_polling()

if __name__ == "__main__":
    main()
