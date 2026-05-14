import os
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from google import genai

TELEGRAM_BOT_TOKEN = "8826980101:AAEn7Ida7S0W2RHhouf5fsdNb4VF2_qP67Y"
GEMINI_API_KEY = "AIzaSyCH7RE7cBJZ688hAWos8HYGL_rD7Z-Eofg"

client = genai.Client(api_key=GEMINI_API_KEY)

async def ai_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"မြန်မာလို သဘာဝကျကျ ဖြေပေးပါ။ User မေးတာ: {user_text}"
    )

    await update.message.reply_text(response.text)

app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, ai_reply))

print("Bot running...")
app.run_polling()
