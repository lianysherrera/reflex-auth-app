import reflex as rx
import sqlalchemy
from sqlalchemy import inspect as sa_inspect

from reflex_auth_app.models.session import Session
from reflex_auth_app.models.user import User
from reflex_auth_app.models.note import Note


def _placeholder_for_column(column: sqlalchemy.Column, dialect) -> object | None:
    compiled_type = column.type.compile(dialect=dialect).upper()

    if "VARCHAR" in compiled_type or "TEXT" in compiled_type or "CHAR" in compiled_type:
        return "(sin definir)"
    if "BOOLEAN" in compiled_type:
        return False
    if "INTEGER" in compiled_type or "FLOAT" in compiled_type or "NUMERIC" in compiled_type:
        return 0
    return None


def _add_missing_columns(engine: sqlalchemy.engine.Engine) -> None:
    inspector = sa_inspect(engine)
    existing_tables = set(inspector.get_table_names())

    for table in User.metadata.sorted_tables:
        if table.name not in existing_tables:
            continue

        existing_columns = {col["name"] for col in inspector.get_columns(table.name)}

        for column in table.columns:
            if column.name in existing_columns:
                continue

            placeholder = _placeholder_for_column(column, engine.dialect)
            column_type_sql = column.type.compile(dialect=engine.dialect)

            with engine.begin() as connection:
                connection.execute(
                    sqlalchemy.text(
                        f"ALTER TABLE {table.name} "
                        f"ADD COLUMN {column.name} {column_type_sql}"
                    )
                )
                if placeholder is not None:
                    connection.execute(
                        sqlalchemy.text(
                            f"UPDATE {table.name} SET {column.name} = :value "
                            f"WHERE {column.name} IS NULL"
                        ),
                        {"value": placeholder},
                    )

            print(
                f"[init_db] Columna nueva detectada: {table.name}.{column.name} "
                f"-- agregada a filas existentes con valor de relleno."
            )


def init_db() -> None:
    engine = rx.model.get_engine()
    User.metadata.create_all(engine)
    _add_missing_columns(engine)