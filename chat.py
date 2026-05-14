import os
import logging
import google.generativeai as genai
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, CommandHandler, filters

# Logging setup (Render log မှာ အမှားရှာရလွယ်အောင်)
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Environment Variables ခေါ်ယူခြင်း
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')

# Gemini AI ကို Setup လုပ်ခြင်း
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash') # gemini-pro ထက် ပိုမြန်တဲ့ flash ကို သုံးထားပါတယ်

# /start command အတွက်
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("မင်္ဂလာပါ။ Gemini AI Bot ကနေ ကြိုဆိုပါတယ်။ ဘာများ ကူညီပေးရမလဲခင်ဗျာ။")

# စာသားတွေကို Gemini နဲ့ ပြန်ဖြေပေးမယ့် Function
async def chat_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    
    try:
        # AI ဆီက အဖြေတောင်းခြင်း
        response = model.generate_content(user_text)
        
        # User ဆီ ပြန်ပို့ခြင်း
        if response.text:
            await update.message.reply_text(response.text)
        else:
            await update.message.reply_text("စိတ်မရှိပါနဲ့၊ ကျွန်တော် ဒီမေးခွန်းကို မဖြေနိုင်လို့ပါ။")
            
    except Exception as e:
        logging.error(f"Error: {e}")
        await update.message.reply_text("တောင်းပန်ပါတယ်။ ခဏတာ အဆင်မပြေမှု ဖြစ်သွားလို့ နောက်မှ ပြန်စမ်းကြည့်ပေးပါ။")

if __name__ == '__main__':
    # Token မရှိရင် Error ပေးဖို့
    if not TELEGRAM_TOKEN or not GEMINI_API_KEY:
        print("Error: API Keys များ မထည့်ရသေးပါ။ Environment Variables ကို စစ်ဆေးပါ။")
    else:
        application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
        
        # Handler များ ထည့်သွင်းခြင်း
        application.add_handler(CommandHandler("start", start))
        application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), chat_handler))
        
        print("Bot စတင် အလုပ်လုပ်နေပါပြီ...")
        application.run_polling()
