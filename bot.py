import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import API_ID, API_HASH, BOT_TOKEN, DB_CHANNEL_ID, WELCOME_PIC, ADMIN_ID

app = Client("ChannelBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start") & filters.private)
async def start(client, message):
    await message.reply_photo(photo=WELCOME_PIC, caption="👋 Hello! Movie ka naam bhejo.")

@app.on_message(filters.text & filters.private & ~filters.command(["start"]))
async def search_file(client, message):
    query = message.text
    status = await message.reply_text("🔍 Searching...")
    
    async for msg in client.search_messages(chat_id=DB_CHANNEL_ID, query=query):
        if msg.document or msg.video:
            buttons = InlineKeyboardMarkup([[InlineKeyboardButton("📥 Download", callback_data=f"get_{msg.id}")]])
            await status.delete()
            await message.reply_text(f"✅ Found: {msg.caption or 'Movie'}", reply_markup=buttons)
            return
    await status.edit("❌ Nahi mili.")

@app.on_callback_query(filters.regex("^get_"))
async def callback_handler(client, query):
    # Yeh line ab ekdum simple hai
    parts = query.data.split("_")
    msg_id = int(parts)
    
    sent = await client.copy_message(chat_id=query.message.chat.id, from_chat_id=DB_CHANNEL_ID, message_id=msg_id)
    await query.message.reply_text("⚠️ 5 minute mein delete ho jayega!")
    asyncio.create_task(delete_after(sent))

async def delete_after(message):
    await asyncio.sleep(300)
    try: await message.delete()
    except: pass

app.run()
