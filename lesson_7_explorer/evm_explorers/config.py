import os

from dotenv import load_dotenv

load_dotenv()

ETHEREUM_API_KEY = str(os.getenv('ETHEREUM_API_KEY'))
