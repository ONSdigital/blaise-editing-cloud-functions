import logging

from sqlalchemy import text

from services.database_connection_service import DatabaseConnectionService


class CaseService:
    def __init__(self, database_connection_service: DatabaseConnectionService) -> None:
        self._database_connection_service = database_connection_service

    def copy_cases(self, questionnaire_name: str) -> tuple[str, int]:
        try:
            logging.info(f"Running Cloud Function - 'copy_cases' for {questionnaire_name}")
            questionnaire_table_name = f"{questionnaire_name}_Form"
            unedited_table_name = f"{questionnaire_name}_UNEDITED_Form"

            sql_database_engine = self._database_connection_service.get_database()

            with sql_database_engine.connect() as sql_connection:
                if not sql_database_engine.dialect.has_table(sql_connection, unedited_table_name):
                    sql_command = text(f"CREATE TABLE {unedited_table_name} \
                                                LIKE {questionnaire_table_name};")
                    sql_connection.execute(sql_command)

                sql_command = text(f"INSERT INTO {unedited_table_name} \
                                                SELECT * from {questionnaire_table_name} \
                                                WHERE IFNULL(QEdit_edited, 0) <> 1 \
                                                ON DUPLICATE KEY UPDATE \
                                                Serial_Number=VALUES(Serial_Number), \
                                                QEdit_LastUpdated=VALUES(QEdit_LastUpdated), \
                                                DataStream=VALUES(DataStream);")
                sql_connection.execute(sql_command)
                sql_connection.commit()

            logging.info(f"Finished Running Cloud Function - 'copy_cases' for {questionnaire_name}")

        except Exception as err:
            return f"Failed to transfer data with the following error: {err}", 500

        return "Done", 200
