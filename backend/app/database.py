from urllib.parse import urlparse

from peewee import PostgresqlDatabase
from app.config import settings


def _db_connect_kwargs():
    url = settings.database_url
    if url:
        u = url.replace("postgresql+psycopg2://", "postgresql://")
        p = urlparse(u)
        path = (p.path or "").lstrip("/").split("?")[0]
        return {
            "database": path or settings.db_name,
            "host": p.hostname or settings.db_host,
            "port": p.port or settings.db_port,
            "user": p.username or settings.db_user,
            "password": p.password if p.password is not None else settings.db_password,
        }
    return {
        "database": settings.db_name,
        "host": settings.db_host,
        "port": settings.db_port,
        "user": settings.db_user,
        "password": settings.db_password,
    }


_kw = _db_connect_kwargs()
database = PostgresqlDatabase(
    _kw["database"],
    host=_kw["host"],
    port=_kw["port"],
    user=_kw["user"],
    password=_kw["password"],
    autorollback=True,
)

db = database

def get_db():
    """FastAPI dependency – mở / đóng connection theo từng request."""
    try:
        database.connect(reuse_if_open=True)
        yield database
    finally:
        if not database.is_closed():
            database.close()
