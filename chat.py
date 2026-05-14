import os
import logging
import google.generativeai as genai
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, CommandHandler, filters

logging.basicConfig(level=logging.INFO)

TELEGRAM_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')

genai.configure(api_key=GEMINI_API_KEY)

# ရနိုင်တဲ့ model တွေကို log ထဲမှာ စစ်ဆေးဖို့
try:
    available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    logging.info(f"Available Models: {available_models}")
except Exception as e:
    logging.error(f"Could not list models: {e}")

# Model ကို ရွေးချယ်ခြင်း (Flash မရရင် Pro ကို သုံးမယ်)
def get_model():
    try:
        # gemini-1.5-flash-latest ကို အရင်စမ်းမယ်
        return genai.GenerativeModel('gemini-1.5-flash-latest')
    except:
        # အဆင်မပြေရင် Stable ဖြစ်တဲ့ gemini-pro ကို သုံးမယ်
        return genai.GenerativeModel('gemini-pro')

model = get_model()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Gemini Bot အဆင်သင့်ဖြစ်ပါပြီ!")

async def chat_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        # စာပြန်ဖို့ ကြိုးစားခြင်း
        response = model.generate_content(update.message.text)
        await update.message.reply_text(response.text)
    except Exception as e:
        logging.error(f"Chat Error: {e}")
        # Error တက်ရင် model နာမည်ကို ခဏပြောင်းပြီး ပြန်စမ်းတာမျိုး လုပ်နိုင်ပါတယ်
        await update.message.reply_text("ခဏလေးနော်၊ တစ်ခုခု မှားနေလို့ပါ။")

if __name__ == '__main__':
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), chat_handler))
    
    print("Bot is running...")
    application.run_polling()
