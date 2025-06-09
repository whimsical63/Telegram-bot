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

    # Paste your cookies here as a Python dict
    cookies = {
        "SPC_F": "eti72Ozj1NdTP9wIj5oyShw6sYaEjcnz",
        "REC_T_ID": "44f2e556-ec78-11ef-a7f1-227ea9f9056a",
        "SPC_CLIENTID": "eti72Ozj1NdTP9wIsnzhemystngwxjfo",
        "__LOCALE__null": "PH",
        "csrftoken": "jNJ4GgoEwQJHBGJ6QF2fT1ql7mFVsrMW",
        "_sapid": "314fd811224f6a763412141344516746ae54937fa9731375a2222da5",
        "_QPWSDCXHZQA": "aafefdaa-4810-4c54-dbd4-d2c58ece78fe",
        "REC7iLP4Q": "24e1a966-3a7a-4e0a-a440-a3d62c0dd504",
        "SPC_SI": "jZUuaAAAAABSYVlsNE9paCxkfAIAAAAAOWVnRFhDclo=",
        "SPC_SEC_SI": "v1-dTd1emI5ajZKQTZOUkM4MUsmeqfTGiJzZ065t3DQSgrqdwJkU4zHA62KCej/mzwsAYm5YlcMxHSFye7il7zPN384jfYikl7XCAPR9q/GcwM=",
        "SPC_P_V": "EbofM8U+S2BQAACFER1hUMHauGhKkTsFfL4d0WNTwp/lxLUTWlqdJJw=",
        "SPC_ST": ".ZXVKWEc0REJ4cXVyVllhabBtNOdR/wzOe9ZxvPRw2Dysvojv2N8KbqX63cyt6gZtQMq2nsk+HKo8UIjSMKi9yEAiMvNw9OqEBGrLYw7maiFTa2cLg5jK1q/M0hR7+rTXImbsNjEwj7nFc5CIPgODUuTLcpSbBLKD9WMbWg3epFV56/y19Rf64uuuBw7n+EWGlXyZFaerbdcXEIIcMeA1uJru5rG5iCg0BZsU53jRY4ujYSZIv0WDpPo/fi0LZvDk",
        "SPC_U": "66572765",
        "SPC_R_T_ID": "NEy0Z5csebkNfs/uphA3TchJxX4j7/tHc7NRbmPAjSqEs3lgFfDfBVFzaHO2MGJSiapcG6ArL+Yq5RwwIUVu0nY7gpeyJJHatZ8nNnKkeWZM2RoLG968+xd/KdSg4To2fcM91wR2auPGqNlxE+rRjjCelofukEcA52lR9rljKu0=",
        "SPC_R_T_IV": "Zm41VXdIcGxzZ2N1eWw0eg==",
        "SPC_T_ID": "NEy0Z5csebkNfs/uphA3TchJxX4j7/tHc7NRbmPAjSqEs3lgFfDfBVFzaHO2MGJSiapcG6ArL+Yq5RwwIUVu0nY7gpeyJJHatZ8nNnKkeWZM2RoLG968+xd/KdSg4To2fcM91wR2auPGqNlxE+rRjjCelofukEcA52lR9rljKu0=",
        "SPC_T_IV": "Zm41VXdIcGxzZ2N1eWw0eg==",
        "SPC_IA": "1",
        "SPC_CDS_CHAT": "7bff6d30-5f02-4d49-a576-ccf0b2d8b925",
        "AC_CERT_D": "U2FsdGVkX1+bMu8dLiuf60/QVKh3cXyh6MwW4EeDRrYzq3YgLw/uIkOStMIv0HzRhz2ObgZUrOQ9/wFcMnWgG/e0N8tLKhlea+jCqak8nVwgjXTUlI+PATK7Dt59RFyoBxvHlRGWET76plI7vTY6sPnDnNUf8xNxDA2pRAlkQZO11Wxk84gzr0v3bJ0pFjKn+bz7y6flI8zmOT/HWFX6Tptbh8jIvVf5LRkr4A4StiitqFLrjwHIql8RqmSEI/6i+ws7divUjRMhCrpRfsh8HK8kQFNFP8rHDkdELpq3xYZnXHAdPYKcseMgqQsU6oTErFBwi/tddx9+8C/zN8uTHKwmLcRTz5A5TX0CFECR3aVnbSlWsDf8bpy9+KLbemaW+njW/p7ENzoZh6Hdx5WEv08gMvysWVGngaHkoVzhIMad0mjEDnHWKIDWZ4HDXJlqAtSG/aKazhV9vW7rej6JTLAglc90DG8Djla9NatGDl8TW3YMGQtUCAX7DwH40EgaALKJIl3EFG4NUMF13xYi0WGt95Kf2YPLbzyDggZ6BFkUo43ZXwJhDUYVVil4Dx0s1Uu7ujHa+aT0KohP4gQSg95L+cWaM+MkfvEAA01dpBXJDfpJ7ir6Lj0A3UBqXcdBYP40jN8sPA50pTeeMYTy1BCWwpHgubafUsyol64nqqvj+86Zf4zHFMD2Y052/jgwty7PwMMmt1c72biHeSyufKCMKYYOQvOYZ30uaiBICy30YZHPepzkFRD6L61tyny9kyHcR5Bs0hzfDul9Yrkke6ipxk9j1OSAb4rEWqVip4Ya94uSOrnem3VTQoEQyPymLR00NX6ySc6hUVO45dE0iJeD1MTPpWoc/tCnO6qBn1P7iO0L5KQYEpNkDc03LTxmovrPbIdTTfbQFnR/EHpFyWOC3LZxBRRTRqjVbPosHcZ4uZl5ureingSqrxq3bfAWhcn2C80TvZ4KHqa09Mr4ck6T44MRdka5PBqsL8ilMkYtqHxG5Eoup5UJNot1WX/ArkXQKP0rRXt6Qb9qIZAsRA01q91sQJmm+jSzwgiJsO+6NOWKdtrGOvM2Ol7LN6LQ8KLbXYk5KE1lGr5nxsyaUQ==",
        "shopee_webUnique_ccd": "P4LuPmkVM0BalsXmUn5c8w%3D%3D%7CZSVThAPil96%2FYy%2FRI3hQennOlDJXSzZ6qN5wgv5cB3clKacJjcTRONZuy5zrAZEoQGNmbw0%2Bd%2BwLtt2tDCA%3D%7CpH5cvPwvtUGi4yFg%7C08%7C3",
        "ds": "2037413a028a5bbf3112bf4c61127824",
        "SPC_EC": ".aldmNW1jcmN0OWdjSnVlRZrWy92ndT0Lir0ObelwsYnH52DcjeUqgMyjLypYZF9M3YaXxHXre54MgJMrlrN8sPuy0a6IeegF+dRAa3LdcQu92vvxPhnHy6N9HL3EnTG7kvNvJZwqJIKdhXE6U+ob74QFDwCeLhh7CyJEKCNu3TdjkmH9cPBc6jCUK/N4WldLqaKAdTf0mXnlV1bxQsFowGfbqLvWNDl8ZlRbL5Ks7sAYkzYexP7iD9mfuzeou1OX"
    }

    try:
        res = requests.get(
            api_url,
            headers={"User-Agent": "Mozilla/5.0"},
            cookies=cookies
        )
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
