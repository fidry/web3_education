import json

# https://pypi.org/project/py-solc-x/0.5.0/
from solcx import compile_standard

from data.config import SOLC_VERSION, simple_number_contract_path


with open(simple_number_contract_path) as f:
    simple_number_contract_text = f.read()

compiled_solidity = compile_standard({
    'language': 'Solidity',
    'sources': {
        'SimpleNumber.sol': {
            'content': simple_number_contract_text,
        }
    },
    'settings': {
        'outputSelection': {
            '*': {
                '*': ['abi', 'metadata', 'evm.bytecode', 'evm.sourceMap']
            }
        }
    }
}, solc_version=SOLC_VERSION)

print(compiled_solidity)

with open('./contracts/compiled_simple_number.json', 'w') as f:
    json.dump(compiled_solidity, f)
