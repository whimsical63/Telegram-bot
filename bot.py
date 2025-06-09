import os
import asyncio
import re
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import requests

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

# Dictionary to store todos
todo_list = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! I'm your personal assistant bot 😊")

async def todo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in todo_list:
        todo_list[user_id] = []

    if context.args:
        task = " ".join(context.args)
        todo_list[user_id].append(task)
        await update.message.reply_text(f"✅ Added to your to-do: {task}")
    else:
        tasks = todo_list[user_id]
        if not tasks:
            await update.message.reply_text("📝 Your to-do list is empty.")
        else:
            formatted = "\n".join(f"{i+1}. {t}" for i, t in enumerate(tasks))
            await update.message.reply_text("📋 Your to-do list:\n" + formatted)



async def weather(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("🌤️ Usage: /weather <city>")
        return

    city = " ".join(context.args)
    api_key = os.getenv("WEATHER_API_KEY")
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    try:
        res = requests.get(url).json()
        if res.get("cod") != 200:
            await update.message.reply_text(f"❌ Could not find weather for '{city}'.")
            return

        desc = res["weather"][0]["description"]
        temp = res["main"]["temp"]
        feels = res["main"]["feels_like"]
        await update.message.reply_text(
            f"📍 Weather in {city}:\n🌡 Temp: {temp}°C\n🤔 Feels like: {feels}°C\n📝 Condition: {desc}"
        )
    except Exception as e:
        await update.message.reply_text("⚠️ Error fetching weather data.")

async def remindme(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 2:
        await update.message.reply_text("⏰ Usage: /remindme <minutes> <message>")
        return

    try:
        delay = int(context.args[0])
        message = " ".join(context.args[1:])
        await update.message.reply_text(f"✅ Reminder set! I'll remind you in {delay} minute(s).")

        await asyncio.sleep(delay * 60)
        await update.message.reply_text(f"⏰ Reminder: {message}")
    except ValueError:
        await update.message.reply_text("⚠️ Please enter a valid number of minutes.")


async def shopee(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("🔗 Please provide a Shopee product link.\nUsage: /shopee <link>")
        return

    url = context.args[0]

    # Extract item_id and shop_id from the URL
    match = re.search(r'i\.(\d+)\.(\d+)', url)
    if not match:
        await update.message.reply_text("❌ Could not extract item_id and shop_id from the link.")
        return

    shop_id, item_id = match.group(1), match.group(2)
    api_url = f"https://shopee.ph/api/v4/pdp/get_pc?item_id={item_id}&shop_id={shop_id}&tz_offset_minutes=480&detail_level=0"

    try:
        res = requests.get(api_url, headers={"User-Agent": "Mozilla/5.0"})
        data = res.json()
        item = data["data"]["item"]

        title = item["title"]
        price_min = item.get("price_min", 0) // 100000
        price_max = item.get("price_max", 0) // 100000

        # If price_min and price_max are the same, show only one price
        if price_min == price_max or price_max == 0:
            price_str = f"₱{price_min}"
        else:
            price_str = f"₱{price_min} - ₱{price_max}"

        await update.message.reply_text(
            f"📦 *{title}*\n💰 Price: {price_str}\n🔗 {url}",
            parse_mode="Markdown"
        )
    except Exception as e:
        await update.message.reply_text("❌ Error while fetching Shopee product info.")
        print("Shopee API error:", e)

# Build the bot
app = ApplicationBuilder().token(BOT_TOKEN).build()

# Add all handlers BEFORE running the bot
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("todo", todo))
app.add_handler(CommandHandler("weather", weather))
app.add_handler(CommandHandler("remindme", remindme))
app.add_handler(CommandHandler("shopee", shopee))

# Start the bot
app.run_polling()
