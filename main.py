import asyncio
from telethon import TelegramClient

# ====== TELEGRAM API ======
api_id = 123456          # your api id
api_hash = "YOUR_API_HASH"
bot_token = "YOUR_BOT_TOKEN"

# ====== MESSAGE ======
MESSAGE = "Hello everyone, this is my message!"

# ====== GROUP / CHANNEL IDS ======
CHAT_IDS = [
    -1001234567890,
    -1009876543210,
    -1001122334455
]

client = TelegramClient("bot", api_id, api_hash)

async def send_messages():
    await client.start(bot_token=bot_token)
    print("Bot started")

    while True:
        for chat in CHAT_IDS:
            try:
                await client.send_message(chat, MESSAGE)
                print(f"Message sent to {chat}")
            except Exception as e:
                print(f"Error sending to {chat}: {e}")

        print("Waiting 1 hour...")
        await asyncio.sleep(3600)  # 1 hour delay


async def main():
    await send_messages()

asyncio.run(main())
