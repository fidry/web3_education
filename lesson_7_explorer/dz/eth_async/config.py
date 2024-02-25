import os

from dotenv import load_dotenv

load_dotenv()

ETHEREUM_API_KEY = str(os.getenv('ETHEREUM_API_KEY'))
ARBITRUM_API_KEY = str(os.getenv('ARBITRUM_API_KEY'))
OPTIMISM_API_KEY = str(os.getenv('OPTIMISM_API_KEY'))
BSC_API_KEY = str(os.getenv('BSC_API_KEY'))
POLYGON_API_KEY = str(os.getenv('POLYGON_API_KEY'))
AVALANCHE_API_KEY = str(os.getenv('AVALANCHE_API_KEY'))
MOONBEAM_API_KEY = str(os.getenv('MOONBEAM_API_KEY'))
FANTOM_API_KEY = str(os.getenv('FANTOM_API_KEY'))
CELO_API_KEY = str(os.getenv('CELO_API_KEY'))
GNOSIS_API_KEY = str(os.getenv('GNOSIS_API_KEY'))
HECO_API_KEY = str(os.getenv('HECO_API_KEY'))
GOERLI_API_KEY = str(os.getenv('GOERLI_API_KEY'))
SEPOLIA_API_KEY = str(os.getenv('SEPOLIA_API_KEY'))
LINEA_API_KEY = str(os.getenv('LINEA_API_KEY'))
BASE_API_KEY = str(os.getenv('BASE_API_KEY'))
