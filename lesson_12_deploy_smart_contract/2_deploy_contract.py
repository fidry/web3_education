"""
Компонент Web3.EthereumTesterProvider() держится на библиотеке eth-tester.
документация eth_tester:
https://pypi.org/project/eth-tester/

В случае ошибки:
"UserWarning: Ethereum Tester: No backend was explicitly set, and no *full* backends were available.
Falling back to the `MockBackend` which does not support all EVM functionality.
Please refer to the `eth-tester` documentation for information on what backends are available and how to set them.
Your py-evm package may need to be updated."
Нужно установить библиотеку py-evm так как на ней держится класс EthereumTester из библиотеки eth-tester
pip install py-evm

"""

from web3 import Web3

from compile_contract import get_abi_and_bytecode_from_contract
from data.config import hello_world_contract_path


w3 = Web3(Web3.EthereumTesterProvider())

# print(w3.eth.default_account)
# print(w3.eth.accounts)
# print(type(w3.eth.accounts[0]))

w3.eth.default_account = w3.eth.accounts[0]
print(w3.eth.default_account)

abi, bytecode = get_abi_and_bytecode_from_contract(contract_path=hello_world_contract_path)

# print(abi)
# print(bytecode)

hello_world_contract = w3.eth.contract(abi=abi, bytecode=bytecode)
print(hello_world_contract)

tx_hash = hello_world_contract.constructor().transact()
print(tx_hash)
print(tx_hash.hex())

tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print(tx_receipt)  # можно подробно посмотреть

hello_world_contract = w3.eth.contract(
    address=tx_receipt.contractAddress,
    abi=abi
)

print(hello_world_contract.functions.sayMessage().call())
# не меняет состояние так как при вызове call мы просто получаем информацию о функции
print(hello_world_contract.functions.setMessage("Buy").call())
print(hello_world_contract.functions.sayMessage().call())

tx_hash = hello_world_contract.functions.setMessage("Buy").transact()
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print(tx_receipt)

print(hello_world_contract.functions.sayMessage().call())

# контракты очень похожи на классы и можно создать несколько инстансев
hello_world_contract2 = w3.eth.contract(abi=abi, bytecode=bytecode)
tx_hash = hello_world_contract2.constructor().transact()
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
hello_world_contract2 = w3.eth.contract(
    address=tx_receipt.contractAddress,
    abi=abi
)

print()
print(hello_world_contract.functions.sayMessage().call())
print(hello_world_contract2.functions.sayMessage().call())
