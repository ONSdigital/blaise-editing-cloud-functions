from unittest.mock import Mock, patch, call, MagicMock

import pytest

from providers.configuration_provider import ConfigurationProvider
from services.blaise_service import BlaiseService
from services.case_service import CaseService
from services.database_service import DatabaseService


class TestCaseService:

    @pytest.fixture()
    def mock_database_service(self) -> DatabaseService:
        return Mock()

    @pytest.fixture()
    def mock_configuration_provider(self) -> ConfigurationProvider:
        return Mock()

    @pytest.fixture()
    def mock_blaise_service(self, mock_configuration_provider) -> BlaiseService:
        return BlaiseService(mock_configuration_provider)

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
    def test_filter_questionnaires_by_survey_type_returns_expected_list_when_given_questionnaire_name(
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
        result = service_under_test.filter_questionnaires_by_survey_type(mock_cases, questionnaire_name)

        # assert
        assert result[0]["name"] == questionnaire_name

    def test_filter_questionnaires_by_survey_type_returns_expected_list_when_given_survey_name(
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
        result = service_under_test.filter_questionnaires_by_survey_type(mock_cases, "FRS")

        # assert
        assert len(result) == 2
        assert result[0]["name"] == "FRS2504A"
        assert result[1]["name"] == "FRS2505A"

    @patch.object(BlaiseService, 'get_questionnaires')
    @patch.object(CaseService, 'copy_cases_for_questionnaire')
    def test_copy_cases_has_calls_for_all_expected_questionnaires(
            self,
            _mock_copy_cases_for_questionnaire,
            _mock_get_questionnaires,
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

        _mock_get_questionnaires.return_value = mock_cases
        # act
        service_under_test.copy_cases("FRS")

        # assert
        assert _mock_copy_cases_for_questionnaire.call_count == 2
        _mock_copy_cases_for_questionnaire.assert_has_calls(
            [call("FRS2504A"),
             call("FRS2505A")]
        )
