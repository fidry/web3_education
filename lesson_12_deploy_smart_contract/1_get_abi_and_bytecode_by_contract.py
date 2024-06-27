"""
remix: https://github.com/ethereum/remix-desktop/releases

В случае ошибки: SolcNotInstalled смотри файл solc_install.py
https://ethereum.stackexchange.com/questions/110405/having-a-problem-with-solc-x-version-solc-0-6-0-has-not-been-installed
"""

from solcx import compile_source

from data.config import SOLC_VERSION, hello_world_contract_path


with open(hello_world_contract_path) as f:
    contract_text = f.read()

compiled_solidity = compile_source(
    source=contract_text,
    output_values=['abi', 'bin'],
    solc_version=SOLC_VERSION
)

print(compiled_solidity)

for key, val in compiled_solidity.items():
    print(key, val)

contract_id, contract_interface = compiled_solidity.popitem()
print('contract_id', contract_id)
print('contract_interface', contract_interface)

abi, bytecode = contract_interface['abi'], contract_interface['bin']

print('abi', abi)
print('bytecode', bytecode)
