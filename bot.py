import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import load_dotenv

load_dotenv

BOT_TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! I'm your personal assistant bot 😊")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))

app.run_polling()

todo_list = {}

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


app.add_handler(CommandHandler("todo", todo))
