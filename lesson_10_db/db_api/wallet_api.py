from db_api.models import Base, Wallet
from db_api.db import DB


def get_wallets(sqlite_query: bool = False) -> list[Wallet]:
    if sqlite_query:
        return db.execute('SELECT * FROM wallets')

    return db.all(entities=Wallet)


def get_wallet(private_key: str, sqlite_query: bool = False) -> Wallet | None:
    if sqlite_query:
        return db.execute('SELECT * FROM wallets WHERE private_key = ?', (private_key,), True)

    return db.one(Wallet, Wallet.private_key == private_key)


# pool_recycle=3600 - это параметр, определяющий,
#   как долго должны оставаться активные подключения в пуле перед их пересозданием.
# check_same_thread устанавливается в False, что позволяет использовать подключение в разных потоках.
db = DB('sqlite:///./wallets.db', echo=False, pool_recycle=3600, connect_args={'check_same_thread': False})
db.create_tables(Base)
