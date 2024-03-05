from aptos_sdk.account import Account

from generate_wallets.utils import PublicKeyUtils


class Wallet:
    def __init__(self, seed_phrase):
        self.seed_phrase = seed_phrase
        self.address, self.private_key = self.generate_aptos_keys()

    def generate_aptos_keys(self):
        pt_seed = PublicKeyUtils(self.seed_phrase)
        keys = Account.load_key(pt_seed.private_key.hex())
        return keys.address(), keys.private_key.hex()

    def __str__(self):
        return f'{self.address}'
