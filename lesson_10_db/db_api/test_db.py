from sqlalchemy import select, or_

from db_api.models import Wallet
from db_api.wallet_api import db


# -------------------------- db.all() --------------------------
# wallets = db.all(Wallet, Wallet.id == 3, Wallet.address.startswith('33'))
# wallets = db.all(Wallet, Wallet.id.is_(3), Wallet.address.startswith('33'))

# stmp = select(Wallet).where(or_(
#     Wallet.address == '3333333',
#     Wallet.address.startswith('22')
# ))
# wallets = db.all(stmp=stmp)
#
# for wallet in wallets:
#     print(wallet.address)


# -------------------------- db.one() --------------------------
# wallet = db.one(Wallet, Wallet.id == 3, Wallet.address.startswith('33'))
# wallet = db.one(Wallet, Wallet.id.is_(3), Wallet.address.startswith('33'))

# stmp = select(Wallet).where(Wallet.address == '3333333')
# wallet = db.one(stmp=stmp)
#
# print(wallet)
