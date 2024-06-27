from web3 import Web3

from compile_contract import get_abi_and_bytecode_from_contract
from deploy.wait_status import wait_tx_status
from deploy.config import private_key


def get_txn_data(w3, account):
    data = {
        'chainId': w3.eth.chain_id,
        'nonce': w3.eth.get_transaction_count(account.address),
        'from': account.address,
        # транзакции с maxFeePerGas не поддерживаются (раскомментируй и проверь)
        # 'maxFeePerGas': w3.eth.max_priority_fee + Web3.to_wei(0.1, "gwei"),
        # 'maxPriorityFeePerGas': w3.eth.max_priority_fee,
        'gasPrice': w3.eth.gas_price,
        'gas': 0
    }

    return data


def send_tx(w3, account, txn) -> str:
    gas = w3.eth.estimate_gas(txn)
    print('gas', gas)

    txn['gas'] = int(gas * 1.5)  # в scroll умножаем иначе получим ошибку "intrinsic gas too low"
    print('increased gas', txn['gas'])

    # раскомментируй, если хочешь, чтобы транзакция отправилась в сеть
    signed_txn = w3.eth.account.sign_transaction(txn, private_key=account._private_key)
    tx_hash = w3.to_hex(w3.eth.send_raw_transaction(signed_txn.rawTransaction))

    return wait_tx_status(w3=w3, tx_hash=tx_hash)


def main():
    rpc = 'https://rpc.ankr.com/scroll/'

    abi, bytecode = get_abi_and_bytecode_from_contract(contract_path='./SimpleNumber.sol')

    w3 = Web3(provider=Web3.HTTPProvider(rpc))

    account = w3.eth.account.from_key(private_key=private_key)
    # print(account.address)

    contract = w3.eth.contract(bytecode=bytecode, abi=abi)
    txn_data = get_txn_data(w3=w3, account=account)
    print('txn_data', txn_data)
    txn = contract.constructor().build_transaction(txn_data)
    print('txn', txn)

    status = send_tx(w3=w3, account=account, txn=txn)
    print(status)


def test_contract():
    contract_address = Web3.to_checksum_address('0xac7366E630A0f1963dDfe431C5dF9A65C8D13be2')

    rpc = 'https://rpc.ankr.com/scroll/'
    abi, bytecode = get_abi_and_bytecode_from_contract(contract_path='./SimpleNumber.sol')
    w3 = Web3(provider=Web3.HTTPProvider(rpc))
    account = w3.eth.account.from_key(private_key=private_key)

    contract = w3.eth.contract(address=contract_address, abi=abi)

    print(contract.functions.getNumber().call())

    tx_params = {
        'chainId': w3.eth.chain_id,
        'nonce': w3.eth.get_transaction_count(account.address),
        'from': account.address,
        'to': contract.address,
        'data': contract.encodeABI('setNumber', args=(
            42,
        )),
        'gasPrice': w3.eth.gas_price,
    }
    # print('tx_params', tx_params)
    gas = w3.eth.estimate_gas(tx_params)
    tx_params['gas'] = gas

    signed_txn = w3.eth.account.sign_transaction(tx_params, private_key=account._private_key)
    tx_hash = w3.to_hex(w3.eth.send_raw_transaction(signed_txn.rawTransaction))

    print(wait_tx_status(w3=w3, tx_hash=tx_hash))

    print(contract.functions.getNumber().call())


if __name__ == '__main__':
    # main()
    test_contract()
