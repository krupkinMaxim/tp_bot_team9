import os
from dotenv import load_dotenv

load_dotenv()  # Загружаем .env

TOKEN = os.getenv("TOKEN")
CMC_API_KEY = os.getenv("CMC_API_KEY")