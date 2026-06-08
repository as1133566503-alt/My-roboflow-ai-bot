from telegram.ext import Application, MessageHandler, filters
from telegram.ext import ContextTypes
from inference_sdk import InferenceHTTPClient

TOKEN = "8798514063:AAHUIBaWbeBvIYRKAlvgoR0xVLj3in_oQqQ"

CLIENT = InferenceHTTPClient(
    api_url="https://detect.roboflow.com",
    api_key="POJWbO5ntJbhoNjilxoE"
POJWb
    "
)

async def handle_photo(update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await update.message.reply_text("جاري عد السيارات...")

        file = await update.message.photo[-1].get_file()
        await file.download_to_drive("image.jpg")

        result = CLIENT.infer("image.jpg", model_id="cars-cars-cars/1")

        predictions = result.get("predictions", [])
        count = len(predictions)

        await update.message.reply_text(f"🚗 عدد السيارات: {count}")

    except Exception as e:
        await update.message.reply_text(f"خطأ: {e}")

app = Application.builder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

print("Bot Running...")
app.run_polling()
