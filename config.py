from dotenv import load_dotenv
from os import getenv
load_dotenv()  # take environment variables from .env.

#загрузить токен
TOKEN :str = getenv("TOKEN")