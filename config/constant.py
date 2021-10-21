import os
from dotenv import load_dotenv

load_dotenv()

DB_URL = os.getenv("DB_URI")
WEBHOOK_URI = os.getenv("WEBHOOK_URI")
EMAIL_API_TOKEN = os.getenv("EMAIL_API_KEY")

#logs colors
ERROR_RED = 15548997
WARN_YELLOW = 16705372
OK_GREEN = 5763719
BLUE = 5793266