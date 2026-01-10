import os
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from flask import Flask
from threading import Thread

# --- কনফিগারেশন ---
TOKEN = '8508407996:AAEvpEs4H7WC77q8go3td1x2gl_QMD_L7DA'
# আপনার নতুন মনিট্যাগ ডিরেক্ট লিঙ্ক (আগেরটি কাজ না করলে এটি ব্যবহার করুন)
MONETAG_LINK = 'https://prizeblass.com/4/8837344' 

# --- রেন্ডার সার্ভার (বট চালু রাখার জন্য) ---
server = Flask('')
@server.route('/')
def home(): return "Earnly Bot is Fully Active!"

def run():
    port = int(os.environ.get('PORT', 8080))
    server.run(host='0.0.0.0', port=port)

# --- বটের মূল মেনু ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.effective_user.first_name
    text = f"স্বাগতম {name}!\nনিচের বাটনগুলো ব্যবহার করে ইনকাম শুরু করুন।"
    
    keyboard = [
        [InlineKeyboardButton("💰 বিজ্ঞাপন দেখুন (ইনকাম)", callback_data='earn')],
        [InlineKeyboardButton("💳 ব্যালেন্স দেখুন", callback_data='balance'),
         InlineKeyboardButton("💸 উইথড্র করুন", callback_data='withdraw')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if update.message:
        await update.message.reply_text(text, reply_markup=reply_markup)
    else:
        await update.callback_query.message.edit_text(text, reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    
    if query.data == 'earn':
        # ইনকাম লজিক (রেন্ডার লগে প্রিন্ট হবে)
        print(f"User {user_id} earned 0.50 TK")
        await query.answer("অভিনন্দন! ০.৫০ টাকা যোগ হয়েছে।", show_alert=True)
        await query.message.reply_text(f"বিজ্ঞাপনটি এখানে দেখুন:\n{MONETAG_LINK}\n\nদেখা শেষ হলে আবার /start দিন।")
        
    elif query.data == 'balance':
        await query.answer()
        await query.message.reply_text("আপনার বর্তমান ব্যালেন্স: ০.৫০ টাকা\n(শিটে আপডেট হতে সময় লাগতে পারে)")
        
    elif query.data == 'withdraw':
        await query.answer()
        await query.message.reply_text("ন্যূনতম উইথড্র ২০ টাকা। আরও ইনকাম করুন!")

if __name__ == '__main__':
    Thread(target=run).start()
    print("Starting Multi-Button Bot...")
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.run_polling()
