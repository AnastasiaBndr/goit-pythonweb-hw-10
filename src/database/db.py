import contextlib
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import (
    AsyncEngine, async_sessionmaker, create_async_engine)
from src.conf.config import config

DATABASE_URL=config.DB_URL

class DatabaseSessionManager:
    def __init__(self, url: str) -> None:
        self._engine: AsyncEngine | None = create_async_engine(url,echo=False)
        self._session_maker: async_sessionmaker = async_sessionmaker(
            autocommit=False, autoflush=False, bind=self._engine)

    @contextlib.asynccontextmanager
    async def session(self):
        if self._session_maker is None:
            raise Exception("Database session is not initialized")
        session = self._session_maker()
        try:
            yield session
        except SQLAlchemyError as e:
            await session.rollback()
            raise
        finally:
            await session.close()


sessionmanager = DatabaseSessionManager(DATABASE_URL)


async def get_db():
    async with sessionmanager.session() as session:
        yield session
