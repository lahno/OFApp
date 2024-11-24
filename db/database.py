from typing import Annotated

from sqlalchemy import String, BIGINT, create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker, mapped_column


sqlite_url = "sqlite:///data.db"

# sync_engine = create_engine(url=settings.database_url_psycopg)
sync_engine = create_engine(url=sqlite_url)

# async_engine = create_async_engine(
#     url=settings.database_url_asyncpg,
#     echo=True,
# )

session_factory = sessionmaker(bind=sync_engine)
# async_session_factory = async_sessionmaker(async_engine)

int_pk = Annotated[BIGINT, mapped_column(primary_key=True)]
big_int = BIGINT
str_256 = Annotated[str, 256]
str_55 = Annotated[str, 55]
str_15 = Annotated[str, 15]


class Base(DeclarativeBase):
    type_annotation_map = {
        str_256: String(256),
        str_55: String(55),
        str_15: String(15),
        int_pk: BIGINT,
        big_int: BIGINT,
    }

    repr_cols_num = 3
    repr_cols: tuple = tuple()
