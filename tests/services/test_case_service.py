from unittest.mock import Mock
from typing import Any, Dict, List

import pytest

from services.case_service import CaseService


class TestCaseService:

    @pytest.fixture()
    def mock_database_service(self):
        return Mock()

    @pytest.fixture()
    def mock_blaise_service(self):
        return Mock()

    @pytest.fixture()
    def service_under_test(self, mock_database_service, mock_blaise_service) -> CaseService:
        return CaseService(mock_database_service, mock_blaise_service)

    @pytest.mark.parametrize(
        "questionnaire_name",
        ["FRS2504A",
         "FRS2505A",
         "LCF2504A",
         "LCF2505A"],
    )
    def test_filter_questionnaires_by_wildcard_returns_expected_list_when_given_questionnaire_name(
            self,
            questionnaire_name,
            service_under_test,
    ):
        # arrange
        mock_cases = [{"name": "FRS2504A",
                       "id": "1234"},
                      {"name": "FRS2505A",
                       "id": "2345"},
                      {"name": "LCF2504A",
                       "id": "3456"},
                      {"name": "LCF2505A",
                       "id": "4567"}]
        # act
        result = service_under_test.filter_questionnaires_by_wildcard(mock_cases, questionnaire_name)

        # assert
        assert result[0]["name"] == questionnaire_name

    def test_filter_questionnaires_by_wildcard_returns_expected_list_when_given_survey_name(
            self,
            service_under_test,
    ):
        # arrange
        mock_cases = [{"name": "FRS2504A",
                       "id": "1234"},
                      {"name": "FRS2505A",
                       "id": "2345"},
                      {"name": "LCF2504A",
                       "id": "3456"},
                      {"name": "LCF2505A",
                       "id": "4567"}]
        # act
        result = service_under_test.filter_questionnaires_by_wildcard(mock_cases, "FRS")

        # assert
        assert result[0]["name"] == "FRS2504A"
        assert result[1]["name"] == "FRS2505A"
