from sqlalchemy import create_engine

from db_api.models import Base


engine = create_engine('sqlite:///wallets.db', echo=True)
Base.metadata.create_all(engine)
