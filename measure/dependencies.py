# Any common dependencies for the measure microservice
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost/ahya_os"

# Sync engine and session setup
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Async engine and session setup
async_engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(
    async_engine, expire_on_commit=False, class_=AsyncSession
)

Base = declarative_base()


# Sync database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Async database dependency
async def get_async_db():

    async_db = AsyncSessionLocal()
    try:
        yield async_db
    finally:
        await async_db.close()