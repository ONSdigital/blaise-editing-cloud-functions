from sqlalchemy import text, Connection, Engine
from services.database_connection_service import DatabaseConnectionService


class DatabaseService:
    def __init__(self, database_connection_service: DatabaseConnectionService) -> None:
        self._database_engine: Engine = database_connection_service.get_database()

    @property
    def database(self) -> Engine:
        return self._database_engine

    def table_exists(self, connection: Connection, table_name: str):
        return self._database_engine.dialect.has_table(connection, table_name)

    def create_table(self, connection: Connection, unedited_table_name: str, questionnaire_table_name: str):
        connection.execute(self.create_table_command(unedited_table_name, questionnaire_table_name))

    def copy_cases(self, connection: Connection, unedited_table_name: str, questionnaire_table_name: str):
        connection.execute(self.copy_cases_command(unedited_table_name, questionnaire_table_name))

    @staticmethod
    def create_table_command(unedited_table_name: str, questionnaire_table_name: str):
        return text(f"CREATE TABLE {unedited_table_name} \
                    LIKE {questionnaire_table_name};")

    @staticmethod
    def copy_cases_command(unedited_table_name: str, questionnaire_table_name: str):
        return text(f"INSERT INTO {unedited_table_name} \
                    SELECT * from {questionnaire_table_name} \
                    WHERE IFNULL(QEdit_edited, 0) <> 1 \
                    ON DUPLICATE KEY UPDATE \
                    Serial_Number=VALUES(Serial_Number), \
                    QEdit_LastUpdated=VALUES(QEdit_LastUpdated), \
                    DataStream=VALUES(DataStream);")
