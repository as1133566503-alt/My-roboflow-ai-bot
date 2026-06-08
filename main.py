from telegram.ext import Application, MessageHandler, filters
from telegram import Update
from telegram.ext import ContextTypes
from inference_sdk import InferenceHTTPClient

TOKEN = "8798514063:AAHUIBaWbeBvIYRKAlvgoR0xVLj3in_oQqQ"

CLIENT = InferenceHTTPClient(
    api_url="https://serverless.roboflow.com",
    api_key="POJWbO5ntJbhoNjilxoE"


)

def find_predictions(data):
    if isinstance(data, dict):
        if "predictions" in data:
            return data["predictions"]
        for value in data.values():
            found = find_predictions(value)
            if found:
                return found
    elif isinstance(data, list):
        for item in data:
            found = find_predictions(item)
            if found:
                return found
    return []

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await update.message.reply_text("جاري عد السيارات...")

        file = await update.message.photo[-1].get_file()
        await file.download_to_drive("image.jpg")

        result = CLIENT.run_workflow(
            workspace_name="s-workspace-t8tcz",
            workflow_id="detect-count-and-visualize",
            images={"image": "image.jpg"},
            use_cache=True
        )

        predictions = find_predictions(result)
        count = len(predictions)

        await update.message.reply_text(f"🚗 عدد السيارات: {count}")

    except Exception as e:
        await update.message.reply_text(f"صار خطأ: {e}")

app = Application.builder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

print("Bot Running...")
app.run_polling()
