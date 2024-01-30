import os
import sys
from pathlib import Path

from dotenv import load_dotenv


load_dotenv()


if getattr(sys, 'frozen', False):
    ROOT_DIR = Path(sys.executable).parent.absolute()
else:
    ROOT_DIR = Path(__file__).parent.parent.absolute()

ABIS_DIR = os.path.join(ROOT_DIR, 'data', 'abis')

PRIVATE_KEY = str(os.getenv('PRIVATE_KEY'))
