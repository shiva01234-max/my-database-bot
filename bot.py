import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import API_ID, API_HASH, BOT_TOKEN, DB_CHANNEL_ID, WELCOME_PIC, ADMIN_ID

app = Client("ChannelBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Start Command
@app.on_message(filters.command("start") & filters.private)
async def start(client, message):
    text = f"👋 Hello **{message.from_user.first_name}**!\n\nMain ek Movie Finder Bot hoon. Movie ka naam bhejo aur link pao!"
    await message.reply_photo(photo=WELCOME_PIC, caption=text)

# Movie Search aur Button logic
@app.on_message(filters.text & filters.private & ~filters.command(["start"]))
async def search_file(client, message):
    query = message.text
    status = await message.reply_text("🔍 **Searching...**")
    
    # Buttons create karna
    async for msg in client.search_messages(chat_id=DB_CHANNEL_ID, query=query):
        if msg.document or msg.video:
            # Movie ka naam file se utha rahe hain
            file_name = msg.caption or msg.document.file_name or "Movie File"
            
            # Inline Button
            buttons = InlineKeyboardMarkup([
                [InlineKeyboardButton("📥 Click here to Download", callback_data=f"get_{msg.id}")]
            ])
            
            await status.delete()
            await message.reply_text(f"✅ **Movie Found:** `{file_name}`\n\nDownload karne ke liye niche button dabayein:", reply_markup=buttons)
            return

    await status.edit("❌ **Sorry, movie nahi mili.**")

# Button click handle karna
@app.on_callback_query(filters.regex("^get_"))
async def callback_handler(client, query):
    msg_id = int(query.data.split("_"))
    
    # File copy karna
    sent = await client.copy_message(chat_id=query.message.chat.id, from_chat_id=DB_CHANNEL_ID, message_id=msg_id)
    await query.message.reply_text("⚠️ **Yeh file 5 minute mein delete ho jayegi!**")
    
    # Auto-delete
    asyncio.create_task(delete_after_delay(sent, 300))

async def delete_after_delay(message, delay=300):
    await asyncio.sleep(delay)
    try: await message.delete()
    except: pass

app.run()
