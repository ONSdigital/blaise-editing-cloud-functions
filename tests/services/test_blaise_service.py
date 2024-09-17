import logging
from unittest import mock
from unittest.mock import Mock

import blaise_restapi
import pytest

from services.blaise_service import BlaiseService
from utilities.custom_exceptions import BlaiseError


class TestBlaiseService:
    @pytest.fixture()
    def mock_case_1(self):
        return {
            "name": "FRS2504A",
            "id": "25615bf2-f331-47ba-9d05-6659a513a1f2",
            "serverParkName": "gusty",
            "installDate": "2024-04-24T09:49:34.2685322+01:00",
            "status": "Active",
            "dataRecordCount": 0,
            "hasData": False,
            "blaiseVersion": "5.9.9.2735",
            "nodes": [
                {"nodeName": "blaise-gusty-mgmt", "nodeStatus": "Active"},
                {"nodeName": "blaise-gusty-data-entry-1", "nodeStatus": "Active"},
                {"nodeName": "blaise-gusty-data-entry-2", "nodeStatus": "Active"},
            ],
        }

    @pytest.fixture()
    def mock_case_2(self):
        return {
            "name": "FRS2505A",
            "id": "54965gh5-s549-96qf-5s16-5496f515g2d6",
            "serverParkName": "gusty",
            "installDate": "2025-01-01T10:50:23.2685322+01:00",
            "status": "Active",
            "dataRecordCount": 0,
            "hasData": False,
            "blaiseVersion": "5.9.9.2735",
            "nodes": [
                {"nodeName": "blaise-gusty-mgmt", "nodeStatus": "Active"},
                {"nodeName": "blaise-gusty-data-entry-1", "nodeStatus": "Active"},
                {"nodeName": "blaise-gusty-data-entry-2", "nodeStatus": "Active"},
            ],
        }

    @pytest.fixture()
    def mock_configuration_provider(self):
        return Mock()

    @pytest.fixture()
    def blaise_service(self, mock_configuration_provider) -> BlaiseService:
        return BlaiseService(mock_configuration_provider)

    @mock.patch.object(blaise_restapi.Client, "get_all_questionnaires_for_server_park")
    def test_get_questionnaires_returns_a_list_of_dictionaries_containing_questionnaire_info(
            self,
            _mock_rest_api_client_get_all_questionnaires_for_server_park,
            blaise_service,
            mock_case_1,
            mock_case_2
    ):
        # Arrange
        _mock_rest_api_client_get_all_questionnaires_for_server_park.return_value = [mock_case_1, mock_case_2]

        # Act
        result = blaise_service.get_questionnaires()

        # Assert
        assert len(result) == 2
        assert isinstance(result, list)

        assert isinstance(result[0], dict)
        assert result[0]["name"] == mock_case_1["name"]
        assert result[0]["id"] == mock_case_1["id"]
        assert result[0]["serverParkName"] == mock_case_1["serverParkName"]

        assert isinstance(result[1], dict)
        assert result[1]["name"] == mock_case_2["name"]
        assert result[1]["id"] == mock_case_2["id"]
        assert result[1]["serverParkName"] == mock_case_2["serverParkName"]

    @mock.patch.object(blaise_restapi.Client, "get_all_questionnaires_for_server_park")
    def test_get_questionnaire_logs_the_correct_information(
            self,
            _mock_rest_api_client_get_all_questionnaires_for_server_park,
            blaise_service,
            caplog,
            mock_case_1,
            mock_case_2
    ):
        # Arrange
        _mock_rest_api_client_get_all_questionnaires_for_server_park.return_value = [mock_case_1, mock_case_2]

        # Act
        with caplog.at_level(logging.INFO):
            blaise_service.get_questionnaires()

        # Assert
        assert (
                   "root",
                   logging.INFO,
                   "Got questionnaires",
               ) in caplog.record_tuples

    @mock.patch.object(blaise_restapi.Client, "get_all_questionnaires_for_server_park")
    def test_get_questionnaire_logs_error_and_raises_blaise_questionnaire_error_exception(
            self,
            mock_rest_api_client_get_all_questionnaires_for_server_park,
            blaise_service,
            caplog
    ):
        # Arrange
        mock_rest_api_client_get_all_questionnaires_for_server_park.side_effect = Exception(
            "DFS had to end their sale"
        )

        # Act
        with pytest.raises(BlaiseError) as err:
            blaise_service.get_questionnaires()

        # Assert
        error_message = (
            "Exception caught in get_questionnaires(). "
            "Error getting questionnaires: DFS had to end their sale"
        )
        assert err.value.args[0] == error_message
        assert (
                   "root",
                   logging.ERROR,
                   error_message,
               ) in caplog.record_tuples
