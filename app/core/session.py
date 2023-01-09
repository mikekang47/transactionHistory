from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

engine = create_engine(
    "mysql+pymysql://{username}:{password}@{host}:{port}/{name}?charset=utf8mb4".format(
        username=settings.MYSQL_USER,
        password=settings.MYSQL_PASSWORD.get_secret_value(),
        host=settings.MYSQL_HOST,
        port=settings.MYSQL_PORT,
        name=settings.MYSQL_DB,
    )
)

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False
)

Base = declarative_base()
