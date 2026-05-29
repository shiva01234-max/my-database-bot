import asyncio
from pyrogram import Client, filters
import os

# Server se configuration utha rahe hain (yahan 0 mat badalna)
API_ID = int(os.environ.get("API_ID", "0"))
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
DB_CHANNEL_ID = int(os.environ.get("DB_CHANNEL_ID", "0"))
WELCOME_PIC = os.environ.get("WELCOME_PIC", "https://images.unsplash.com/photo-1536440136628-849c177e76a1?w=800")

app = Client("ChannelBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start") & filters.private)
async def start(client, message):
    welcome_text = (
        f"👋 **Hello {message.from_user.first_name}!**\n\n"
        "Main is channel ka official Database Bot hoon.\n"
        "🎬 Mujhe kisi bhi movie ka **Sahi Naam** bhejien, main aapko file de dunga.\n\n"
        "⚠️ **DHYAN RAKHEIN:** Movie milne ke baad file 5 minute mein delete ho jayegi!"
    )
    try:
        await message.reply_photo(photo=WELCOME_PIC, caption=welcome_text)
    except Exception:
        await message.reply_text(welcome_text)

async def delete_after_delay(message, delay=300):
    await asyncio.sleep(delay)
    try:
        await message.delete()
    except Exception as e:
        print(f"Delete error: {e}")

@app.on_message(filters.text & filters.private)
async def search_file(client, message):
    query = message.text
    status_msg = await message.reply_text("🔍 **Dhoondh raha hoon...**")
    
    found = 0
    try:
        async for msg in client.search_messages(chat_id=DB_CHANNEL_ID, query=query):
            if msg.document or msg.video or msg.audio:
                found += 1
                sent_file = await msg.copy(chat_id=message.chat.id)
                warning_msg = await message.reply_text("⚠️ **5 minute mein delete ho jayega!**")
                asyncio.create_task(delete_after_delay(sent_file, 300))
                asyncio.create_task(delete_after_delay(warning_msg, 300))
        
        if found > 0:
            await status_msg.delete()
        else:
            await status_msg.edit("❌ **Nahi mili!** Spelling check kar le.")
    except Exception as e:
        await status_msg.edit(f"⚠️ **Error:** {e}")

print("Bot tyaar hai...")
app.run()
