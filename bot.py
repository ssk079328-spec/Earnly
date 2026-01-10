import os
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from flask import Flask
from threading import Thread

# --- কনফিগারেশন ---
TOKEN = '8508407996:AAHt-1hDETJdAsX2TJvGw19GuG0eqnkfSDU'
MONETAG_LINK = 'https://prizeblass.com/4/8837344'
# আপনার শিট লিঙ্ক (Apps Script-এর মাধ্যমে ডাটা পাঠানোর জন্য ব্যবহার হবে)
SHEET_URL = 'https://docs.google.com/spreadsheets/d/1LkqmsHTESG1n2vh_LlgEKol1WWPAXdBCBqmWWibce6M/edit'

# --- রেন্ডারকে জাগিয়ে রাখার সার্ভার ---
server = Flask('')

@server.route('/')
def home():
    return "Earnly Bot is Online and Running!"

def run():
    port = int(os.environ.get('PORT', 8080))
    server.run(host='0.0.0.0', port=port)

# --- বটের মূল ফাংশন ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.effective_user.first_name
    keyboard = [[InlineKeyboardButton("💰 ইনকাম শুরু করুন", callback_data='earn')]]
    await update.message.reply_text(
        f"স্বাগতম {name}!\nবিজ্ঞাপন দেখে আয় করতে নিচের বাটনে ক্লিক করুন।", 
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def earn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = str(query.from_user.id)
    name = query.from_user.first_name
    
    # এখানে আমরা ইউজারের ডাটা প্রিন্ট করছি যাতে আপনি রেন্ডার লগে সেটি দেখতে পান
    print(f"User: {name} (ID: {user_id}) earned 0.50 TK")
    
    await query.answer("অভিনন্দন! ০.৫০ টাকা সফলভাবে যোগ হয়েছে।", show_alert=True)
    await query.message.reply_text(f"আপনার বিজ্ঞাপন লিঙ্ক: {MONETAG_LINK}\nপরের বার ইনকাম করতে আবার /start দিন।")

if __name__ == '__main__':
    # সার্ভার ব্যাকগ্রাউন্ডে চালু করা
    Thread(target=run).start()
    
    # টেলিগ্রাম বট সেটআপ
    print("Starting bot...")
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(earn, pattern='earn'))
    application.run_polling()
