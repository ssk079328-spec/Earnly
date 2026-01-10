import os
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from flask import Flask
from threading import Thread

# --- কনফিগারেশন ---
# আপনার নতুন টোকেন
TOKEN = '8508407996:AAEvpEs4H7WC77q8go3td1x2gl_QMD_L7DA'

# আপনার নতুন মনিট্যাগ লিঙ্কসমূহ
AD_LINKS = [
    'https://otieu.com/4/9855404',
    'https://otieu.com/4/10074134'
]

# --- রেন্ডার সার্ভার (বট ২৪ ঘণ্টা চালু রাখার জন্য) ---
server = Flask('')

@server.route('/')
def home():
    return "Earnly Bot is Active and Running!"

def run():
    port = int(os.environ.get('PORT', 8080))
    server.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- বটের মূল মেনু ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.effective_user.first_name
    text = (
        f"স্বাগতম {name}!\n\n"
        "💰 প্রতি বিজ্ঞাপনে আয়: ০.৫০ টাকা\n"
        "💸 মিনিমাম উইথড্র: ২০ টাকা\n\n"
        "নিচের বাটনগুলো ব্যবহার করে কাজ শুরু করুন:"
    )
    
    keyboard = [
        [InlineKeyboardButton("💰 বিজ্ঞাপন ১ (Earn)", callback_data='earn_1')],
        [InlineKeyboardButton("💰 বিজ্ঞাপন ২ (Earn)", callback_data='earn_2')],
        [InlineKeyboardButton("💳 ব্যালেন্স", callback_data='balance'),
         InlineKeyboardButton("💸 উইথড্র", callback_data='withdraw')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(text, reply_markup=reply_markup)

# --- বাটন ক্লিকের কাজ ---
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    
    if query.data.startswith('earn'):
        # কোন বিজ্ঞাপনটি ক্লিক করা হয়েছে তা নির্ধারণ
        link_index = 0 if query.data == 'earn_1' else 1
        link = AD_LINKS[link_index]
        
        # রেন্ডার লগে ইনকাম রেকর্ড হবে
        print(f"User {user_id} earned 0.50 TK from Ad {link_index + 1}")
        
        await query.answer("অভিনন্দন! ০.৫০ টাকা আয় হয়েছে।", show_alert=True)
        await query.message.reply_text(
            f"আপনার বিজ্ঞাপন লিঙ্কটি এখানে দেখুন:\n{link}\n\n"
            "দেখা শেষ হলে আবার /start দিন।"
        )
        
    elif query.data == 'balance':
        await query.answer()
        await query.message.reply_text("📊 আপনার বর্তমান ব্যালেন্স: ০.৫০ টাকা")
        
    elif query.data == 'withdraw':
        await query.answer()
        await query.message.reply_text("❌ দুঃখিত! আপনার ব্যালেন্স ২০ টাকার কম।")

if __name__ == '__main__':
    keep_alive() # সার্ভার চালু
    print("Bot is starting with new token and links...")
    
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    
    # কনফ্লিক্ট এরর এড়াতে drop_pending_updates=True রাখা হয়েছে
    application.run_polling(drop_pending_updates=True)
