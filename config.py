import os
import dotenv
load_dotenv()
class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    GOOGLE_CLIENT_ID =os.getenv("your_google_client_id")
    GOOGLE_CLIENT_SECRET = "your_google_client_secret"
