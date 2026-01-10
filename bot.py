import os
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from flask import Flask
from threading import Thread

# --- তথ্য সেটআপ ---
TOKEN = '8508407996:AAF1e6hcJXR4Gy7I_t6vOxPoE6spDnV2NJY'
MONETAG_LINK = 'https://prizeblass.com/4/8837344' 

# আপনার গুগল শিটের পুরো পাবলিক লিঙ্ক
SHEET_LINK = 'https://docs.google.com/spreadsheets/d/1LkqmsHTESG1n2vh_LlgEKol1WWPAXdBCBqmWWibce6M/edit?usp=drivesdk'

# --- রেন্ডার ফ্রি টায়ারের জন্য ফ্লাস্ক সার্ভার ---
server = Flask('')

@server.route('/')
def home():
    return "Bot is Running!"

def run():
    port = int(os.environ.get('PORT', 8080))
    server.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- বটের মূল কাজ ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.effective_user.first_name
    keyboard = [[InlineKeyboardButton("💰 ইনকাম শুরু করুন", callback_data='earn')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        f"স্বাগতম {name}!\n\nবিজ্ঞাপন দেখে আয় করতে নিচের বাটনে ক্লিক করুন।", 
        reply_markup=reply_markup
    )

async def earn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = str(query.from_user.id)
    name = query.from_user.first_name
    
    # ইউজারকে ইনকাম দেওয়া
    await query.answer("অভিনন্দন! ০.৫০ টাকা রেকর্ড করা হয়েছে।", show_alert=True)
    await query.message.reply_text(
        f"আপনার বিজ্ঞাপনটি এখানে দেখুন:\n{MONETAG_LINK}\n\nআবার ইনকাম করতে /start দিন।"
    )
    print(f"User {name} ({user_id}) clicked the ad.")

if __name__ == '__main__':
    keep_alive() # রেন্ডারকে জাগিয়ে রাখার জন্য
    print("Bot is starting...")
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(earn, pattern='earn'))
    application.run_polling()
