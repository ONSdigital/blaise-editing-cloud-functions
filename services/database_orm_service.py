from sqlalchemy import Engine, inspect


class DatabaseOrmService:
    def check_table_exists(self, database: Engine, table_name: str, schema_name: str) -> bool:
        return inspect(database).has_table(table_name, schema=schema_name)
