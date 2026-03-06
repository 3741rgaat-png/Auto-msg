import asyncio
import json
from telethon import TelegramClient
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

api_id = 123456
api_hash = "API_HASH"
bot_token = "BOT_TOKEN"

message = ""
delay = 180
running = False

def load_groups():
    try:
        with open("groups.json","r") as f:
            return json.load(f)
    except:
        return []

def save_groups():
    with open("groups.json","w") as f:
        json.dump(groups,f)

groups = load_groups()

client = TelegramClient("session", api_id, api_hash)

async def sender():
    global running
    while True:
        if running and message:
            for g in groups:
                try:
                    await client.send_message(g, message)
                    print("Sent to", g)
                except Exception as e:
                    print("Error:", e)

                await asyncio.sleep(45)

        await asyncio.sleep(delay)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot Ready")

async def add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    g = context.args[0]
    if g not in groups:
        groups.append(g)
        save_groups()
    await update.message.reply_text("Group Added")

async def addmany(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lines = update.message.text.split("\n")[1:]
    added = 0

    for g in lines:
        g = g.strip()
        if g and g not in groups:
            groups.append(g)
            added += 1

    save_groups()

    await update.message.reply_text(f"{added} Groups Added")

async def setmsg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global message
    message = " ".join(context.args)
    await update.message.reply_text("Message Set")

async def settime(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global delay
    delay = int(context.args[0])
    await update.message.reply_text("Time Updated")

async def run(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global running
    running = True
    await update.message.reply_text("Auto Sending Started")

async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global running
    running = False
    await update.message.reply_text("Stopped")

async def main():

    await client.start()

    app = ApplicationBuilder().token(bot_token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("add", add))
    app.add_handler(CommandHandler("addmany", addmany))
    app.add_handler(CommandHandler("setmsg", setmsg))
    app.add_handler(CommandHandler("settime", settime))
    app.add_handler(CommandHandler("run", run))
    app.add_handler(CommandHandler("stop", stop))

    asyncio.create_task(sender())

    await app.run_polling()

asyncio.run(main())
