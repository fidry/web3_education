import time

from web3.exceptions import TransactionNotFound


def wait_tx_status(w3, tx_hash: str, max_wait_time=300) -> str | None:
    start_time = time.time()
    while True:
        try:
            receipts = w3.eth.get_transaction_receipt(tx_hash)
            status = receipts.get("status")
            if status == 1:
                return f"Successfully transaction: {tx_hash}"
            elif status is None:
                time.sleep(0.3)
            else:
                return f"Failed transaction:{tx_hash}!"
        except TransactionNotFound:
            if time.time() - start_time > max_wait_time:
                return f"Failed transaction: {tx_hash}!"
            time.sleep(3)
