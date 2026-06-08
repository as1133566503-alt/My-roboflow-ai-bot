from telegram.ext import Application, MessageHandler, filters
from telegram import Update
from telegram.ext import ContextTypes

TOKEN = 8798514063:AAHUIBaWbeBvIYRKAlvgoR0xVLj3in_oQqQ

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot is running")

app = Application.builder().token(TOKEN).build()

app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

print("Bot Running...")
app.run_polling()
