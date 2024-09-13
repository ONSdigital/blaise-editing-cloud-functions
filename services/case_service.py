from services.database_service import DatabaseService


class CaseService:
    def __init__(self, database_service: DatabaseService) -> None:
        self._database_service = database_service

    def copy_cases(self, questionnaire_name: str):
        questionnaire_table_name = f"{questionnaire_name}_Form"
        unedited_table_name = f"{questionnaire_name}_UNEDITED_Form"

        with self._database_service.database.begin() as connection:
            if not self._database_service.table_exists(connection, unedited_table_name):
                self._database_service.create_table(connection, unedited_table_name, questionnaire_table_name)

            self._database_service.copy_cases(connection, unedited_table_name, questionnaire_table_name)

