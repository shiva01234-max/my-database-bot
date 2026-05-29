import os

API_ID = int(os.environ.get("API_ID", "36191326"))
API_HASH = os.environ.get("API_HASH", "db41b3636e96ac3ae96561010f0ceeca")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8863078609:AAFP6Do_XeGa3_mFBw55adzK4ekdKHTDSvk")

# Admin ID: Yahan apni Telegram User ID daal (taki koi aur bot ko control na kar sake)
ADMIN_ID = int(os.environ.get("ADMIN_ID", "6024953191")) 

# Movie Channel ID: Yahan apne channel ki ID daal
DB_CHANNEL_ID = int(os.environ.get("DB_CHANNEL_ID", "-1003773475761"))

WELCOME_PIC = os.environ.get("WELCOME_PIC", "https://images.unsplash.com/photo-1536440136628-849c177e76a1?w=800")
