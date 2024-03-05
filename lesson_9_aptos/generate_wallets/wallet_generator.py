import csv
import os
from datetime import datetime
from mnemonic import Mnemonic
from generate_wallets.wallet import Wallet

from data.config import FILES_DIR


class WalletGenerator:
    @staticmethod
    def generate_wallet() -> Wallet:
        seed_phrase = Mnemonic('english').generate()
        return Wallet(seed_phrase)


wallets_rows = []
wallets_count = int(input('How many wallets to generate: '))
for _ in range(wallets_count):
    wallet = WalletGenerator.generate_wallet()
    wallets_rows.append([wallet.address, wallet.private_key, wallet.seed_phrase])

with open(os.path.join(FILES_DIR, f"wallets_{str(datetime.now()).replace(' ', '_')}.csv"), 'w') as f:
    writer = csv.writer(f)
    writer.writerow(['address', 'private_key', 'seed'])
    writer.writerows(wallets_rows)
