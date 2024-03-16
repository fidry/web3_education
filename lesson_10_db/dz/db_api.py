from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from data.config import WALLETS_DB

db_uri = f'sqlite+aiosqlite:///{WALLETS_DB}'

async_engine = create_async_engine(
    db_uri,
    pool_pre_ping=True,
    echo=False,
)

AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    autoflush=False,
    future=True,
)


class Session:
    def __init__(self):
        self.session = AsyncSessionLocal()
        # self.session = AsyncSession(bind=async_engine)

    async def __aenter__(self):
        return self.session

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        try:
            await self.session.commit()
        except Exception as e:
            await self.session.rollback()
            raise e
        finally:
            await self.session.close()
