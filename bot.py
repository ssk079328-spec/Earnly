import os
import gspread
from google.oauth2.service_account import Credentials
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from flask import Flask
from threading import Thread

# --- আপনার দেওয়া তথ্য ---
TOKEN = '8508407996:AAF1e6hcJXR4Gy7I_t6vOxPoE6spDnV2NJY'
# মনিট্যাগ ডিরেক্ট লিঙ্ক (আমি আপনার কোড থেকে লিঙ্কটি সাজিয়ে দিচ্ছি)
MONETAG_LINK = 'https://prizeblass.com/4/8837344' 

# --- গুগল শিট কানেক্ট ---
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = Credentials.from_service_account_file('creds.json', scopes=scope)
client = gspread.authorize(creds)
sheet = client.open("Earnly").sheet1

# --- রেন্ডারকে জাগিয়ে রাখার জন্য সার্ভার ---
app = Flask('')

@app.route('/')
def home():
    return "Earnly Bot is Online!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- বটের মূল কাজ ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    name = update.effective_user.first_name
    
    # শিটে ইউজার চেক ও অ্যাড করা
    try:
        users = sheet.col_values(1)
        if user_id not in users:
            sheet.append_row([user_id, name, 0, "", 0])
    except Exception as e:
        print(f"Sheet Error: {e}")
        
    keyboard = [[InlineKeyboardButton("💰 বিজ্ঞাপন দেখুন (০.৫০ টাকা)", callback_data='earn')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        f"স্বাগতম {name}!\n\nপ্রতিটি বিজ্ঞাপন দেখার জন্য আপনি ০.৫০ টাকা পাবেন। ইনকাম শুরু করতে নিচের বাটনে ক্লিক করুন।", 
        reply_markup=reply_markup
    )

async def earn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = str(query.from_user.id)
    
    # শিটে ব্যালেন্স আপডেট করা
    try:
        cell = sheet.find(user_id)
        current_val = sheet.cell(cell.row, 3).value
        bal = float(current_val) if current_val else 0.0
        sheet.update_cell(cell.row, 3, bal + 0.50)
        
        await query.answer("অভিনন্দন! আপনার ব্যালেন্সে ০.৫০ টাকা যোগ হয়েছে।", show_alert=True)
        await query.message.reply_text(
            f"আপনার বিজ্ঞাপনটি এখানে দেখুন:\n{MONETAG_LINK}\n\nআবার ইনকাম করতে /start দিন।"
        )
    except Exception as e:
        await query.answer("দুঃখিত, কোনো সমস্যা হয়েছে। আবার চেষ্টা করুন।")

if __name__ == '__main__':
    keep_alive() # রেন্ডারের জন্য
    
    # টেলিগ্রাম বট রান করা
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(earn, pattern='earn'))
    application.run_polling()
