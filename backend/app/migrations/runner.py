"""
Apply SQL migrations in this package (modules named NNNN_*.py with upgrade(db)).
Usage: python -m app.migrations.runner upgrade
"""
from __future__ import annotations

import importlib
import sys
from pathlib import Path

from app.database import database

_MIGRATION_TABLE = "app_schema_migrations"


def _ensure_table() -> None:
    database.execute_sql(
        f"""
        CREATE TABLE IF NOT EXISTS {_MIGRATION_TABLE} (
            id         SERIAL PRIMARY KEY,
            name       VARCHAR(255) NOT NULL UNIQUE,
            applied_at TIMESTAMPTZ NOT NULL DEFAULT now()
        )
        """
    )


def _applied() -> set[str]:
    _ensure_table()
    cursor = database.execute_sql(f"SELECT name FROM {_MIGRATION_TABLE}")
    return {row[0] for row in cursor.fetchall()}


def _discover() -> list[str]:
    here = Path(__file__).resolve().parent
    paths = sorted(here.glob("[0-9][0-9][0-9][0-9]_*.py"))
    return [p.stem for p in paths]


def upgrade() -> None:
    database.connect(reuse_if_open=True)
    try:
        done = _applied()
        for name in _discover():
            if name in done:
                continue
            mod = importlib.import_module(f"app.migrations.{name}")
            with database.atomic():
                mod.upgrade(database)
                database.execute_sql(
                    f"INSERT INTO {_MIGRATION_TABLE} (name) VALUES (%s)",
                    (name,),
                )
            print(f"[migrations] applied {name}")
    finally:
        if not database.is_closed():
            database.close()


def main() -> None:
    cmd = sys.argv[1] if len(sys.argv) > 1 else "upgrade"
    if cmd == "upgrade":
        upgrade()
    else:
        raise SystemExit(f"unknown command: {cmd!r} (use: upgrade)")


if __name__ == "__main__":
    main()
