import asyncio
from pyrogram import Client, filters

# Apni API_ID, API_HASH aur BOT_TOKEN yahan daalo
# Best practice: inko environment variables mein rakho
api_id = "36191326"
api_hash = "db41b3636e96ac3ae96561010f0ceeca"
bot_token = "8863078609:AAFP6Do_XeGa3_mFBw55adzK4ekdKHTDSvk"

app = Client("my_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

@app.on_message(filters.command("start"))
async def start_command(client, message):
    # Tumhara custom branding message
    text = (
        "**Welcome to savi.stream!**\n\n"
        "Main ek database bot hoon.\n"
        "Developed by **Shiva**"
    )
    # Agar logo bhejna hai toh yahan photo ka link ya file_id daalo
    await message.reply_text(text)

async def main():
    await app.start()
    print("Bot started successfully!")
    await asyncio.Event().wait() # Bot ko chalate rehne ke liye

if __name__ == "__main__":
    try:
        app.run(main())
    except Exception as e:
        print(f"Error: {e}")
