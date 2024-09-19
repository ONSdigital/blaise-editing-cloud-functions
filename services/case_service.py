import logging
from typing import Any, Dict, List

from services.blaise_service import BlaiseService
from services.database_service import DatabaseService


class CaseService:
    def __init__(self, database_service: DatabaseService, blaise_service: BlaiseService) -> None:
        self._database_service = database_service
        self._blaise_service = blaise_service

    def copy_cases(self, survey_type: str):
        questionnaires = self._blaise_service.get_questionnaires()

        for questionnaire in self.filter_questionnaires_by_survey_type(questionnaires, survey_type):
            self.copy_cases_for_questionnaire(questionnaire["name"])

    def copy_cases_for_questionnaire(self, questionnaire_name: str):
        logging.info(f"copy_cases_to_unedited for '{questionnaire_name}'")
        questionnaire_table_name = f"{questionnaire_name}_Form"
        unedited_table_name = f"{questionnaire_name}_UNEDITED_Form"

        with self._database_service.database.begin() as connection:
            if not self._database_service.table_exists(connection, unedited_table_name):
                self._database_service.create_table(connection, unedited_table_name, questionnaire_table_name)

            self._database_service.copy_cases(connection, unedited_table_name, questionnaire_table_name)

    @staticmethod
    def filter_questionnaires_by_survey_type(questionnaires: List[Dict[str, Any]],
                                             survey_type: str) -> List[Dict[str, Any]]:
        return list(
            filter(lambda questionnaire: questionnaire["name"].startswith(survey_type),
                   questionnaires))
