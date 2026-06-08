from telegram.ext import Application, MessageHandler, filters
from telegram import Update
from telegram.ext import ContextTypes
from inference_sdk import InferenceHTTPClient
from PIL import Image, ImageDraw
import traceback

TOKEN = "8798514063:AAHUIBaWbeBvIYRKAlvgoR0xVLj3in_oQqQ"

CLIENT = InferenceHTTPClient(
    api_url="https://serverless.roboflow.com",
  
    api_key="POJWbO5ntJbhoNjilxoE"


)

def find_predictions(data):
    if isinstance(data, dict):
        if "predictions" in data:
            return data["predictions"]
        for v in data.values():
            r = find_predictions(v)
            if r:
                return r
    if isinstance(data, list):
        for item in data:
            r = find_predictions(item)
            if r:
                return r
    return []

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await update.message.reply_text("وصلت الصورة ✅ جاري الفحص...")

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

        img.save("result.jpg")

        with open("result.jpg", "rb") as photo:
            await update.message.reply_photo(
                photo=photo,
                caption=f"🚗 عدد السيارات: {count}"
            )

    except Exception as e:
        await update.message.reply_text("صار خطأ:\n" + str(e))

app = Application.builder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

print("Bot Running...")
app.run_polling()
