from telegram.ext import Application, MessageHandler, filters
from telegram import Update
from telegram.ext import ContextTypes
from inference_sdk import InferenceHTTPClient

TOKEN = "8798514063:AAHUIBaWbeBvIYRKAlvgoR0xVLj3in_oQqQ"


CLIENT = InferenceHTTPClient(
    api_url="https://serverless.roboflow.com",
    api_key="حط_api_key_هنا"
)

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo = await update.message.photo[-1].get_file()
    await photo.download_to_drive("image.jpg")

    result = CLIENT.run_workflow(
        workspace_name="s-workspace-t8tcz",
        workflow_id="detect-count-and-visualize",
        images={
            "image": "image.jpg"
        },
        use_cache=True
    )

    count = len(result[0]["predictions"])

    await update.message.reply_text(f"🚗 عدد السيارات: {count}")

app = Application.builder().token(TOKEN).build()

app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

print("Bot Running...")
app.run_polling()
inference-sdk
