import os

# Yahan apni details daal (yadi tu abhi nahi daalna chahta toh 0 rehne de, hum baad mein hosting par daal denge)
API_ID = int(os.environ.get("API_ID", "0"))
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
DB_CHANNEL_ID = int(os.environ.get("DB_CHANNEL_ID", "0"))

WELCOME_PIC = os.environ.get("WELCOME_PIC", "https://images.unsplash.com/photo-1536440136628-849c177e76a1?w=800")
