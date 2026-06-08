from telegram.ext import Application, MessageHandler, filters
from telegram import Update
from telegram.ext import ContextTypes
from inference_sdk import InferenceHTTPClient
from PIL import Image, ImageDraw
import os

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
            if found is not None:
                return found
    if isinstance(data, list):
        for item in data:
            found = find_predictions(item)
            if found is not None:
                return found
    return []

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("استلمت الصورة، جاري العد والتحديد...")

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

    img = Image.open("image.jpg").convert("RGB")
    draw = ImageDraw.Draw(img)

    for p in predictions:
        x = p.get("x")
        y = p.get("y")
        w = p.get("width")
        h = p.get("height")

        if x and y and w and h:
            left = x - w / 2
            top = y - h / 2
            right = x + w / 2
            bottom = y + h / 2
            draw.rectangle([left, top, right, bottom], width=4)
            draw.text((left, top), "car", fill=(255, 255, 255))

    img.save("result.jpg")

    await update.message.reply_photo(
        photo=open("result.jpg", "rb"),
        caption=f"🚗 عدد السيارات: {count}"
    )

app = Application.builder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

print("Bot Running...")
app.run_polling()
