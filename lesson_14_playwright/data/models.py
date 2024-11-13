class Wallet:
    def __init__(self, address: str, private_key: str):
        self.address = address
        self.private_key = private_key

    def __repr__(self):
        return (f"Wallet("
                f"address='{self.address}', "
                f"private_key='{self.private_key[:3]}***{self.private_key[-3:]}'"
                f")")
