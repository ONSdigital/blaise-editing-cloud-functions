from unittest import mock

import pytest

from appconfig.sql_configuration import Config
from main import copy_cases_to_unedited
import logging


class TestMainCopyCasesToUneditedHandleConfigStep:

    @pytest.mark.parametrize(
        "instance_name, database_username, database_password",
        [
            (None, None, None),
            ("", None, None),
            (None, "", None),
            (None, None, ""),
            (None, "", ""),
            ("", None, ""),
            ("", "", None),
            ("", "", ""),
        ],
    )
    @mock.patch("appconfig.config.Config.from_env")
    def test_create_donor_case_returns_message_and_400_status_code_when_all_configs_are_missing(
            self, mock_config, instance_name, database_username, database_password, caplog
    ):
        # Arrange
        mock_config.return_value = Config(instance_name=instance_name,
                                          database_username=database_username,
                                          database_password=database_password)

        # Act
        with caplog.at_level(logging.ERROR):
            result = copy_cases_to_unedited()

        # Assert
        error_message = (
            "Error copying cases to unedited: "
            "Missing required values from config: ['instance_name', 'database_username', 'database_password']"
        )
        assert result == (error_message, 400)
        assert (
                   "root",
                   logging.ERROR,
                   error_message,
               ) in caplog.record_tuples

    @pytest.mark.parametrize(
        "instance_name",
        [None, ""],
    )
    @mock.patch("appconfig.config.Config.from_env")
    def test_create_donor_case_returns_message_and_400_status_code_when_instance_name_config_is_missing(
            self, mock_config, instance_name, caplog
    ):
        # Arrange
        mock_config.return_value = Config(instance_name=instance_name,
                                          database_username="test_user",
                                          database_password="test_password")

        # Act
        with caplog.at_level(logging.ERROR):
            result = copy_cases_to_unedited()

        # Assert
        error_message = (
            "Error copying cases to unedited: "
            "Missing required values from config: ['instance_name']"
        )
        assert result == (error_message, 400)
        assert (
                   "root",
                   logging.ERROR,
                   error_message,
               ) in caplog.record_tuples

    @pytest.mark.parametrize(
        "database_username",
        [None, ""],
    )
    @mock.patch("appconfig.config.Config.from_env")
    def test_create_donor_case_returns_message_and_400_status_code_when_database_username_config_is_missing(
            self, mock_config, database_username, caplog
    ):
        # Arrange
        mock_config.return_value = Config(instance_name="test_instance_name",
                                          database_username=database_username,
                                          database_password="test_password")

        # Act
        with caplog.at_level(logging.ERROR):
            result = copy_cases_to_unedited()

        # Assert
        error_message = (
            "Error copying cases to unedited: "
            "Missing required values from config: ['database_username']"
        )
        assert result == (error_message, 400)
        assert (
                   "root",
                   logging.ERROR,
                   error_message,
               ) in caplog.record_tuples

    @pytest.mark.parametrize(
        "database_password",
        [None, ""],
    )
    @mock.patch("appconfig.config.Config.from_env")
    def test_create_donor_case_returns_message_and_400_status_code_when_database_password_config_is_missing(
            self, mock_config, database_password, caplog
    ):
        # Arrange
        mock_config.return_value = Config(instance_name="test_instance_name",
                                          database_username="test_user",
                                          database_password=database_password)

        # Act
        with caplog.at_level(logging.ERROR):
            result = copy_cases_to_unedited()

        # Assert
        error_message = (
            "Error copying cases to unedited: "
            "Missing required values from config: ['database_password']"
        )
        assert result == (error_message, 400)
        assert (
                   "root",
                   logging.ERROR,
                   error_message,
               ) in caplog.record_tuples