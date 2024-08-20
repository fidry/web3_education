from pydantic import BaseModel, RootModel


class Wallet(BaseModel):
    address: str
    private_key: str

    def __repr__(self):
        return f"Wallet(address='{self.address}', private_key='{self.private_key[:3]}***{self.private_key[-3:]}')"


class Wallets(RootModel[list[Wallet]]):
    pass
