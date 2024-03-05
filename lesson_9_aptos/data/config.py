from loguru import logger
import os
import sys
from pathlib import Path


if getattr(sys, 'frozen', False):
    ROOT_DIR = Path(sys.executable).parent.absolute()
else:
    ROOT_DIR = Path(__file__).parent.parent.absolute()

FILES_DIR = os.path.join(ROOT_DIR, 'files')
ABIS_DIR = os.path.join(ROOT_DIR, 'abis')

CACH_PATH = os.path.join(FILES_DIR, 'cach.dat')
DEBUG_PATH = os.path.join(FILES_DIR, 'debug.log')
SETTINGS_PATH = os.path.join(FILES_DIR, 'settings.json')
PRIVATE_KEYS_PATH = os.path.join(FILES_DIR, 'private_keys.csv')
WALLETS_DB = os.path.join(FILES_DIR, 'wallets.db')

logger.add(f'{DEBUG_PATH}', format='{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}', level='DEBUG')
