from sqlalchemy import select
from sqlalchemy.orm import Session

from db_api.models import Wallet
from db_api.db_init import engine


session = Session(engine)

# 1 способ удаления
# удалит объект сразу (мы его даже посмотреть не сможем)
# q = session.query(Wallet).filter_by(address='000000000').delete()
# session.commit()


# # 2 способ удаления
# # получили нужные нам объекты и достали только первый из них
# stmp = select(Wallet).where(Wallet.address == '2222222')
# wallet = session.scalars(stmp).first()
# print('address:', wallet.address)
# # удаляем этот объект
# session.delete(wallet)
# session.commit()
