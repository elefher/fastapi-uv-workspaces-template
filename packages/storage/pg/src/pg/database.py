import contextlib
import logging
from typing import AsyncIterator, Optional

from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from pg.models import Base

class DatabaseNotInitializedError(Exception):
    """Exception raised when the DatabaseSessionManager is used before being initialized."""


class DatabaseSessionManager:
    """
    Manages asynchronous database connections and sessions for a FastAPI application using SQLAlchemy.

    This class encapsulates the creation and disposal of an async engine and sessionmaker.
    """

    def __init__(self) -> None:
        self._engine: Optional[AsyncEngine] = None
        self._sessionmaker: Optional[async_sessionmaker] = None
        self.logger = logging.getLogger(__name__)

    def init(self, host: str, **engine_kwargs) -> None:
        """
        Initialize the async engine and sessionmaker with the provided database connection string.

        Args:
            host (str): The database connection string.
            **engine_kwargs: Additional keyword arguments to pass to create_async_engine (e.g. echo, pool_size).
        """
        if not host:
            raise ValueError("A valid connection string must be provided.")
        # You might add more validation of the connection string here.
        self._engine = create_async_engine(host, **engine_kwargs)
        self._sessionmaker = async_sessionmaker(autocommit=False, bind=self._engine)
        self.logger.info("Database engine initialized with host: %s", host)

    async def close(self) -> None:
        """
        Dispose of the engine and reset the sessionmaker.
        """
        if self._engine is None:
            raise DatabaseNotInitializedError(
                "DatabaseSessionManager is not initialized"
            )
        await self._engine.dispose()
        self.logger.info("Database engine disposed")
        self._engine = None
        self._sessionmaker = None

    @contextlib.asynccontextmanager
    async def connect(self) -> AsyncIterator[AsyncConnection]:
        """
        Provide a transactional async connection.

        Yields:
            AsyncConnection: An active asynchronous connection.

        Raises:
            DatabaseNotInitializedError: If the engine is not initialized.
        """
        if self._engine is None:
            raise DatabaseNotInitializedError(
                "DatabaseSessionManager is not initialized"
            )
        async with self._engine.begin() as connection:
            try:
                yield connection
            except Exception as e:
                await connection.rollback()
                self.logger.error("Error during connection; rolling back: %s", e)
                raise

    @contextlib.asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        """
        Provide an asynchronous session context.

        Yields:
            AsyncSession: An active asynchronous session.

        Raises:
            DatabaseNotInitializedError: If the sessionmaker is not initialized.
        """
        if self._sessionmaker is None:
            raise DatabaseNotInitializedError(
                "DatabaseSessionManager is not initialized"
            )
        session: AsyncSession = self._sessionmaker()
        try:
            yield session
            # Optionally, you could call await session.commit() here if auto-commit is desired.
        except Exception as e:
            await session.rollback()
            self.logger.error("Error during session; rolling back: %s", e)
            raise
        finally:
            await session.close()
            self.logger.info("Session closed")

    async def create_all(self, connection: AsyncConnection, base: Base) -> None:
        """
        Create all tables defined in the declarative base metadata.

        Args:
            connection (AsyncConnection): The connection to use for schema creation.
        """
        await connection.run_sync(base.metadata.create_all)
        self.logger.info("All tables created")

    async def drop_all(self, connection: AsyncConnection, base: Base) -> None:
        """
        Drop all tables defined in the declarative base metadata.

        Args:
            connection (AsyncConnection): The connection to use for dropping schema.
        """
        await connection.run_sync(base.metadata.drop_all)
        self.logger.info("All tables dropped")


sessionmanager = DatabaseSessionManager()


async def get_session() -> AsyncIterator[AsyncSession]:
    """
    FastAPI dependency to provide a database session.

    Yields:
        AsyncSession: The active database session.
    """
    async with sessionmanager.session() as session:
        yield session


async def init_db() -> DatabaseSessionManager:
    """
    Initialize the database engine.
    """
    from pg.settings import get_settings

    settings = get_settings()
    sessionmanager.init(settings.pg_url)

    # Establish an asynchronous connection
    # Don't use this in production; use alembic migration tool instead
    async with sessionmanager.connect() as connection:
        # Create all tables
        await sessionmanager.create_all(connection, Base)

    return sessionmanager
