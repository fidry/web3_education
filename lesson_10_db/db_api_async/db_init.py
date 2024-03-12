from sqlalchemy import create_engine

from db_api_async.models import Base


engine = create_engine('sqlite:///./wallets.db', echo=False)
Base.metadata.create_all(engine)
