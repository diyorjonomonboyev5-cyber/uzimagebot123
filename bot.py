import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

from openai import OpenAI

# 🔑 API KEY (OpenAI dan olasan)
client = OpenAI(api_key="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")

# 🔑 Telegram Token
TOKEN = "8610613439:AAGaNi2DM65tOeoJoATiMXImsORBXbQNXgE"


# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Salom!\n\n/chat - AI bilan gaplashish\n/image - rasm yaratish"
    )


# 💬 CHAT AI
async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": user_text}
        ]
    )

    answer = response.choices[0].message.content
    await update.message.reply_text(answer)


# 🎨 IMAGE AI
async def image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = " ".join(context.args)

    if not prompt:
        await update.message.reply_text("Misol: /image katta shahar tunda")
        return

    img = client.images.generate(
        model="gpt-image-1",
        prompt=prompt,
        size="1024x1024"
    )

    image_url = img.data[0].url
    await update.message.reply_photo(photo=image_url)


def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("image", image))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

    print("Bot ishlayapti...")
    app.run_polling()


if __name__ == "__main__":
    main()
