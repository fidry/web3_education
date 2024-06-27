import os
import sys
from pathlib import Path


if getattr(sys, 'frozen', False):
    ROOT_DIR = Path(sys.executable).parent.absolute()
else:
    ROOT_DIR = Path(__file__).parent.parent.absolute()

CONTRACTS_DIR = os.path.join(ROOT_DIR, 'contracts')

SOLC_VERSION = '0.8.0'

hello_world_contract_path = os.path.join(CONTRACTS_DIR, 'HelloWorld.sol')
simple_number_contract_path = os.path.join(CONTRACTS_DIR, 'SimpleNumber.sol')
