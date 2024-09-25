# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

# SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost/AhyaOS"

# # Sync engine and session setup
# engine = create_engine(SQLALCHEMY_DATABASE_URL)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# # Async engine and session setup
# async_engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)
# AsyncSessionLocal = sessionmaker(
#     async_engine, expire_on_commit=False, class_=AsyncSession
# )

# # Sync database dependency
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# # Async database dependency
# async def get_async_db():
#     async_db = AsyncSessionLocal()
#     try:
#         yield async_db
#     finally:
#         await async_db.close()


from contextlib import asynccontextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

# SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost/AhyaOS"
# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@localhost/Ahya_OS"
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@localhost/Ahya_OS"
# Sync engine and session setup
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Async engine and session setup
# async_engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)
# AsyncSessionLocal = sessionmaker(
#     async_engine, expire_on_commit=False, class_=AsyncSession
# )

# Sync database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Async database dependency
# async def get_async_db():
#     async_db = AsyncSessionLocal()
#     try:
#         yield async_db
#     finally:
#         await async_db.close()
