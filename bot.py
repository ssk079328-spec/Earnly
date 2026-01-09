import gspread
from google.oauth2.service_account import Credentials
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# সেটআপ (আপনার বটের তথ্য এখানে দিন)
TOKEN = 'আপনার_বট_টোকেন' # @BotFather থেকে পাওয়া টোকেন দিন
MONETAG_LINK = 'আপনার_মনিট্যাগ_লিঙ্ক' # আপনার মনিট্যাগ ডিরেক্ট লিঙ্ক দিন

# গুগল শিট কানেক্ট করা
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = Credentials.from_service_account_file('creds.json', scopes=scope)
client = gspread.authorize(creds)
sheet = client.open("Earnly").sheet1 # আপনার শিটের নাম Earnly হলে এটাই থাকবে

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    name = update.effective_user.first_name
    
    # ইউজার শিটে আছে কিনা চেক করা
    users = sheet.col_values(1)
    if user_id not in users:
        sheet.append_row([user_id, name, 0, "", 0])
        
    keyboard = [[InlineKeyboardButton("📱 বিজ্ঞাপন দেখুন (০.৫০ টাকা)", callback_data='earn')]]
    await update.message.reply_text(f"স্বাগতম {name}!\nইনকাম করতে নিচের বাটনে ক্লিক করুন।", reply_markup=InlineKeyboardMarkup(keyboard))

async def earn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = str(query.from_user.id)
    
    # ব্যালেন্স ০.৫০ বাড়ানো
    cell = sheet.find(user_id)
    bal = float(sheet.cell(cell.row, 3).value or 0)
    sheet.update_cell(cell.row, 3, bal + 0.50)
    
    await query.answer("অভিনন্দন! ০.৫০ টাকা যোগ হয়েছে।", show_alert=True)
    await query.message.reply_text(f"বিজ্ঞাপন দেখতে এখানে ক্লিক করুন: {MONETAG_LINK}")

if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(earn, pattern='earn'))
    app.run_polling()
