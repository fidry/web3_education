import os

from dotenv import load_dotenv

load_dotenv()

OKLINK_API_KEY = str(os.getenv('OKLINK_API_KEY'))
