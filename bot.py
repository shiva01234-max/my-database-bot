import os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# --- CONFIGURATION ---
API_ID = "36191326"        
API_HASH = "db41b3636e96ac3ae96561010f0ceeca"   
BOT_TOKEN = "8863078609:AAFP6Do_XeGa3_mFBw55adzK4ekdKHTDSvk" 
# Database Channel ID 
DB_CHANNEL_ID = "-1003773475761"

# External Media & Links
THANK_YOU_IMAGE = "https://graph.org/file/your_uploaded_savi_ai_image.jpg"
AESTHETIC_QUALITY_IMAGE = "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?q=80&w=1000"
CHANNEL_LINK = "https://t.me/your_movie_channel" 

# --- INITIALIZE BOT ---
app = Client("SaviMovieBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)


# --- START COMMAND ---
@app.on_message(filters.command("start") & filters.private)
async def start_command(client, message):
    welcome_text = (
        f"👋🏻 **Hello {message.from_user.mention}!**\n\n"
        "Welcome to **SAVI.AI Advanced Intelligence** Movie Bot. 🍿\n\n"
        "💬 **Yahan sirf Movie ka sahi naam type karke bhejein.**\n"
        "Main direct hamare private database se aapko high-quality files nikaal kar dunga.\n\n"
        "⚠️ *Note: Faltu messages (hi, hello, etc.) ya galat spelling par bot result nahi dega.*"
    )
    
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🎬 Check Quality Info", callback_data="check_quality"),
            InlineKeyboardButton("💖 Say Thank You", callback_data="say_thanks")
        ],
        [InlineKeyboardButton("📢 Join Our Channel", url=CHANNEL_LINK)]
    ])
    
    await message.reply_text(text=welcome_text, reply_markup=keyboard)


# --- STRICT MOVIE SEARCH & SPELLING MISTAKE HANDLER ---
@app.on_message(filters.text & filters.private)
async def strict_movie_search(client, message):
    movie_query = message.text.strip()
    
    # Ignore commands (jaise /start, /help) taaki normal function disturb na ho
    if movie_query.startswith("/"):
        return

    # Agar user ne bahot chhota text bheja (jaise hi, ok, yo, hlo) jo movie name nahi ho sakta
    if len(movie_query) < 3:
        await message.reply_text(
            "⚠️ **Invalid Input!**\n\n"
            "Kripya sirf movie ka full aur correct naam likhein.\n"
            "Example: `Avatar` ya `Pushpa 2`"
        )
        return

    # Searching status loader
    searching_msg = await message.reply_text("🔍 *Scanning SAVI.AI Database...*")
    results = []
    
    # Private Database channel me scan chalega
    async for msg in client.search_messages(chat_id=DB_CHANNEL_ID, query=movie_query):
        if msg.document or msg.video:
            file_name = msg.document.file_name if msg.document else msg.video.file_name
            results.append([InlineKeyboardButton(f"🎬 {file_name}", callback_data=f"file_{msg.id}")])
            
        if len(results) >= 15: # Max 15 files dikhayega ek baar me
            break

    # Agar files mil gayi database me
    if results:
        await searching_msg.delete() 
        response_text = (
            f"🎯 **Results Found for:** `{movie_query}`\n\n"
            "Niche diye gaye buttons par click karke direct download karein 👇🏻"
        )
        await message.reply_text(text=response_text, reply_markup=InlineKeyboardMarkup(results))
        
    else:
        # ❌ SPELLING MISTAKE / NOT FOUND MESSAGE
        await searching_msg.edit(
            text=(
                f"❌ **Movie Not Found: `{movie_query}`**\n\n"
                "**⚠️ Ho sakta hai aapne Spelling Mistake ki ho!**\n"
                "Sahi tareeke se dhoondhne ke liye in tips ka use karein:\n\n"
                "1️⃣ Google par exact spelling check karein.\n"
                "2️⃣ Movie ka poora naam likhein (e.g., `Bhediya` ke badle `Bhediya 2022`).\n"
                "3️⃣ Extra symbols ya emojis text me na dalein.\n\n"
                "🔄 Please ek baar correct spelling ke sath dobara try karein!"
            ),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📢 Request Movie Here", url=CHANNEL_LINK)]
            ])
        )


# --- BUTTON CLICK HANDLER (Forwarding & Media) ---
@app.on_callback_query()
async def handle_callback(client, callback_query):
    data = callback_query.data
    chat_id = callback_query.message.chat.id
    
    if data == "say_thanks":
        await callback_query.answer("Sending Banner...")
        await client.send_photo(
            chat_id=chat_id,
            photo=THANK_YOU_IMAGE,
            caption="✨ **Thank you for using SAVI.AI Movie Bot!** ✨\n\nEnjoy your premium streaming experience."
        )
        
    elif data == "check_quality":
        await callback_query.answer()
        quality_caption = (
            "⚡ **SAVI.AI PREMIUM QUALITY STANDARDS** ⚡\n\n"
            "Humare database me movies in formats me milti hain:\n"
            "🔹 **4K UHD** Ultra Clean HDR\n"
            "🔹 **1080p Full HD** Bluray [Dual Audio]\n"
            "🔹 **720p HD** Zip / Direct Files"
        )
        await client.send_photo(chat_id=chat_id, photo=AESTHETIC_QUALITY_IMAGE, caption=quality_caption)
        
    elif data.startswith("file_"):
        await callback_query.answer("🚀 Processing File from Database...")
        message_id = int(data.split("_"))
        
        try:
            # File forward/copy system
            await client.copy_message(
                chat_id=chat_id,
                from_chat_id=DB_CHANNEL_ID,
                message_id=message_id
            )
        except Exception:
            await client.send_message(chat_id=chat_id, text="❌ Yeh file send nahi ho paayi. Kripya admin se sampark karein.")


# --- RUN BOT ---
if __name__ == "__main__":
    print("🔥 SAVI.AI Strict Auto-Filter Bot is Live! 🔥")
    app.run()
