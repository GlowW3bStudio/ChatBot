import os
import logging
from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, filters, ContextTypes
from google import genai

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = os.getenv("BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=GEMINI_API_KEY)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("မင်္ဂလာပါ 🤖 မေးချင်တာကို မြန်မာလိုမေးလို့ရပါတယ်။")

async def ai_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=f"""
မင်းက Telegram AI assistant တစ်ယောက်ဖြစ်တယ်။
မြန်မာလို သဘာဝကျကျ၊ ဖော်ရွေပြီး တိုတိုရှင်းရှင်း ဖြေပေးပါ။

User message:
{user_text}
"""
        )

        reply = response.text if response.text else "မဖြေနိုင်သေးပါဘူး 🥲"
        await update.message.reply_text(reply)

    except Exception as e:
        logging.error(f"Gemini Error: {e}")
        await update.message.reply_text(
            "AI server busy ဖြစ်နေပါတယ် 🥲 ခဏနေရင်ပြန်မေးပေးပါ။"
        )

def main():
    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN မရှိပါ။ Render Environment မှာထည့်ပါ။")

    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY မရှိပါ။ Render Environment မှာထည့်ပါ။")

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, ai_reply))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
