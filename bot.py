import asyncio
from pyrogram import Client, filters
from config import API_ID, API_HASH, BOT_TOKEN, DB_CHANNEL_ID, WELCOME_PIC, ADMIN_ID

app = Client("ChannelBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# 1. Sirf Private Chat ke liye filter
private_only = filters.private

# Start command
@app.on_message(filters.command("start") & private_only)
async def start(client, message):
    welcome_text = (
        f"👋 **Hello {message.from_user.first_name}!**\n\n"
        "Main is channel ka Database Bot hoon.\n"
        "🎬 Filmein chahiye? Toh bas mujhe movie ka naam bhejo.\n\n"
        "💡 **Note:** Main sirf yahan DM mein kaam karta hoon, kisi group mein nahi!"
    )
    try:
        await message.reply_photo(photo=WELCOME_PIC, caption=welcome_text)
    except Exception:
        await message.reply_text(welcome_text)

# 2. Movie Search (Sirf Private)
@app.on_message(filters.text & private_only & ~filters.command(["start"]))
async def search_file(client, message):
    query = message.text
    # Admin ke liye check
    if message.from_user.id == ADMIN_ID:
        await message.reply_text("Admin, aapka command received!")
        
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
        
        if found == 0:
            await status_msg.edit("❌ **Nahi mili!** Spelling check kar le.")
        else:
            await status_msg.delete()
    except Exception as e:
        await status_msg.edit(f"⚠️ **Error:** {e}")

async def delete_after_delay(message, delay=300):
    await asyncio.sleep(delay)
    try: await message.delete()
    except: pass

app.run()
