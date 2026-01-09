import os
import gspread
from google.oauth2.service_account import Credentials
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from flask import Flask
from threading import Thread

# --- তথ্য সেটআপ ---
TOKEN = '8508407996:AAF1e6hcJXR4Gy7I_t6vOxPoE6spDnV2NJY'
MONETAG_LINK = 'https://prizeblass.com/4/8837344' 

# --- গুগল শিট কানেক্ট ---
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = Credentials.from_service_account_file('creds.json', scopes=scope)
client = gspread.authorize(creds)
sheet = client.open("Earnly").sheet1

# --- রেন্ডার ফ্রি টায়ারের জন্য ফ্লাস্ক সার্ভার ---
server = Flask('')

@server.route('/')
def home():
    return "Earnly Bot is Online!"

def run():
    # রেন্ডার সাধারণত ১০০০০ বা ৮০৮০ পোর্ট ব্যবহার করে
    port = int(os.environ.get('PORT', 8080))
    server.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- বটের ফাংশন ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    name = update.effective_user.first_name
    
    users = sheet.col_values(1)
    if user_id not in users:
        sheet.append_row([user_id, name, "0", "", "0"])
        
    keyboard = [[InlineKeyboardButton("💰 বিজ্ঞাপন দেখুন (০.৫০ টাকা)", callback_data='earn')]]
    await update.message.reply_text(f"স্বাগতম {name}!\nইনকাম করতে নিচের বাটনে ক্লিক করুন।", reply_markup=InlineKeyboardMarkup(keyboard))

async def earn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = str(query.from_user.id)
    
    try:
        cell = sheet.find(user_id)
        current_val = sheet.cell(cell.row, 3).value
        bal = float(current_val) if current_val else 0.0
        sheet.update_cell(cell.row, 3, bal + 0.50)
        
        await query.answer("অভিনন্দন! ০.৫০ টাকা যোগ হয়েছে।", show_alert=True)
        await query.message.reply_text(f"বিজ্ঞাপন দেখুন: {MONETAG_LINK}\nআবার ইনকাম করতে /start দিন।")
    except Exception as e:
        await query.answer("আবার চেষ্টা করুন।")

if __name__ == '__main__':
    keep_alive() # সার্ভার চালু
    print("Bot is starting...")
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(earn, pattern='earn'))
    app.run_polling()
