import os
import requests
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import load_dotenv

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

# Build the bot
app = ApplicationBuilder().token(BOT_TOKEN).build()

# Add all handlers BEFORE running the bot
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("todo", todo))
app.add_handler(CommandHandler("weather", weather))
app.add_handler(CommandHandler("remindme", remindme))

# Start the bot
app.run_polling()
