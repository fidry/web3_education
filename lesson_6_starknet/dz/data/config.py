import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from loguru import logger


load_dotenv()


if getattr(sys, 'frozen', False):
    ROOT_DIR = Path(sys.executable).parent.absolute()
else:
    ROOT_DIR = Path(__file__).parent.parent.absolute()

ABIS_DIR = os.path.join(ROOT_DIR, 'abis')
FILES_DIR = os.path.join(ROOT_DIR, 'files')

private_key = int(os.getenv('PRIVATE_KEY'), 16)
account_address = int(os.getenv('ACCOUNT_ADDRESS'), 16)
proxy = str(os.getenv('PROXY'))

NODE_URLS = [
    # 'https://starknet-mainnet.public.blastapi.io',
    'https://starknet-mainnet.blastapi.io/02391fda-266d-444e-ab15-90bbbd3d3471/rpc/v0_6'
]

logger.add(
    f'{os.path.join(FILES_DIR, "debug.log")}',
    format='{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}',
    level='SUCCESS'
)
