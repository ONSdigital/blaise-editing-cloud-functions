from typing import Iterator

from sqlalchemy import Connection, text

from services.database_connection_service import DatabaseConnectionService


class DatabaseService:
    def __init__(self, database_connection_service: DatabaseConnectionService) -> None:
        self._database_connection_service = database_connection_service
        self._database_engine = self._database_connection_service.get_database()
        self._connection = None

    @property
    def connection(self):
        if self._connection is None:
            self._connection = self.connect()
        return self._connection

    def connect(self) -> Iterator[Connection]:
        return self._database_engine.begin()

    def table_exists(self, table_name: str):
        return self._database_engine.dialect.has_table(self._connection, table_name)

    def create_table(self, unedited_table_name: str, questionnaire_table_name: str):
        self._connection.execute(self.create_table_command(unedited_table_name, questionnaire_table_name))

    def copy_cases(self, unedited_table_name: str, questionnaire_table_name: str):
        self._connection.execute(self.copy_cases_command(unedited_table_name, questionnaire_table_name))

    @staticmethod
    def create_table_command(unedited_table_name: str, questionnaire_table_name: str) -> text:
        return text(f"CREATE TABLE {unedited_table_name} \
                    LIKE {questionnaire_table_name};")

    @staticmethod
    def copy_cases_command(unedited_table_name: str, questionnaire_table_name: str) -> text:
        return text(f"INSERT INTO {unedited_table_name} \
                    SELECT * from {questionnaire_table_name} \
                    WHERE IFNULL(QEdit_edited, 0) <> 1 \
                    ON DUPLICATE KEY UPDATE \
                    Serial_Number=VALUES(Serial_Number), \
                    QEdit_LastUpdated=VALUES(QEdit_LastUpdated), \
                    DataStream=VALUES(DataStream);")
