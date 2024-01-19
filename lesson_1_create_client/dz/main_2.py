from decimal import Decimal


'''
Token:
    address
    balance
'''

tokens_dict = {
    'ETH': {
        'address': '0x00000000000000000000000000000000000000',
        'balancee': 1000000000000000000
    },
    'USDC': {
        'address': '0xIu67bubyTG23GBybuyb72672367826374gVHH76',
        'balancee': 1000000
    }
}


class Token:
    def __init__(self, name: str, address: str, balance: int):
        name = name.upper()
        self.name = name
        self.address = address
        self.balance = balance

    def __str__(self):
        return f'name: {self.name} | address: {self.address} | balance: {self.balance}'

    def __repr__(self):
        return f'Token(name="{self.name}", address="{self.address}", balance={self.balance})'


class Tokens:
    ETH = Token(name='ETH', address='0x00000000000000000000000000000000000000', balance=1000000000000000000)
    USDC = Token(name='USDC', address='0xIu67bubyTG23GBybuyb72672367826374gVHH76', balance=1000000)


# print(Tokens.USDC.balance)
print(Tokens.ETH)
print(Tokens.USDC)


# class TokenAmount:
#     Wei: int
#     Ether: Decimal
#     decimals: int
#
#     def __init__(self, amount: int | float | str | Decimal, decimals: int = 18, wei: bool = False) -> None:
#         if wei:
#             self.Wei: int = int(amount)
#             self.Ether: Decimal = Decimal(str(amount)) / 10 ** decimals
#
#         else:
#             self.Wei: int = int(Decimal(str(amount)) * 10 ** decimals)
#             self.Ether: Decimal = Decimal(str(amount))
#
#         self.decimals = decimals
#
#     def __str__(self):
#         return f'{self.Ether}'
#
#
# balance = TokenAmount(
#     amount=0.1,
#     decimals=6,
#     wei=False
# )
# print(balance.Ether)
# print(balance.Wei)
