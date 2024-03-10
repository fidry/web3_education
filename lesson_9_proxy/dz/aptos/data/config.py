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

DEBUG_PATH = os.path.join(FILES_DIR, 'debug.log')

logger.add(f'{DEBUG_PATH}', format='{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}', level='DEBUG')
