from contextlib import contextmanager

import flask
import pytest

from appconfig.sql_configuration import SqlConfiguration
from services.validation_service import ValidationService
from tests.helper import get_default_config
from utilities.custom_exceptions import (
    ConfigError, RequestError,
)


@pytest.fixture()
def config() -> SqlConfiguration:
    return get_default_config()


@contextmanager
def does_not_raise(expected_exception):
    try:
        yield

    except expected_exception as error:
        raise AssertionError(f"Raised exception {error} when it should not!")

    except Exception as error:
        raise AssertionError(f"An unexpected exception {error} raised.")


class MockRequest:
    def __init__(self, json_data):
        self.json_data = json_data

    def get_json(self):
        return self.json_data


class TestValidationService:
    def test_validate_config_is_not_empty_does_not_raise_an_exception_when_given_valid_config(self):
        # arrange
        validation_service = ValidationService()
        mock_config = SqlConfiguration(instance_name="test_instance_name",
                                       database_username="test_user",
                                       database_password="test_password")

        # assert
        with does_not_raise(ConfigError):
            validation_service.validate_config_is_not_empty(mock_config)

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
    def test_validate_config_is_not_empty_logs_and_raises_config_error_when_all_config_values_are_missing(
            self, instance_name, database_username, database_password, caplog
    ):
        # arrange
        mock_config = SqlConfiguration(instance_name=instance_name,
                                       database_username=database_username,
                                       database_password=database_password)

        validation_service = ValidationService()

        # act
        with pytest.raises(ConfigError) as err:
            validation_service.validate_config_is_not_empty(mock_config)

        # assert
        error_message = \
            "Missing required values from config: ['instance_name', 'database_username', 'database_password']"
        assert err.value.args[0] == error_message
        assert (
                   "root",
                   40,
                   error_message,
               ) in caplog.record_tuples

    @pytest.mark.parametrize(
        "instance_name",
        [None, ""],
    )
    def test_validate_config_is_not_empty_logs_and_raises_config_error_when_instance_name_is_missing(
            self, instance_name, caplog
    ):
        # arrange
        mock_config = SqlConfiguration(instance_name=instance_name,
                                       database_username="test_user",
                                       database_password="test_password")

        validation_service = ValidationService()

        # act
        with pytest.raises(ConfigError) as err:
            validation_service.validate_config_is_not_empty(mock_config)

        # assert
        error_message = "Missing required values from config: ['instance_name']"
        assert err.value.args[0] == error_message
        assert (
                   "root",
                   40,
                   error_message,
               ) in caplog.record_tuples

    @pytest.mark.parametrize(
        "database_username",
        [None, ""],
    )
    def test_validate_config_is_not_empty_logs_and_raises_config_error_when_database_username_is_missing(
            self, database_username, caplog
    ):
        # arrange
        mock_config = SqlConfiguration(instance_name="test_instance_name",
                                       database_username=database_username,
                                       database_password="test_password")

        validation_service = ValidationService()

        # act
        with pytest.raises(ConfigError) as err:
            validation_service.validate_config_is_not_empty(mock_config)

        # assert
        error_message = "Missing required values from config: ['database_username']"
        assert err.value.args[0] == error_message
        assert (
                   "root",
                   40,
                   error_message,
               ) in caplog.record_tuples

    @pytest.mark.parametrize(
        "database_password",
        [None, ""],
    )
    def test_validate_config_is_not_empty_logs_and_raises_config_error_when_database_password_is_missing(
            self, database_password, caplog
    ):
        # arrange
        mock_config = SqlConfiguration(instance_name="test_instance_name",
                                       database_username="test_user",
                                       database_password=database_password)

        validation_service = ValidationService()

        # act
        with pytest.raises(ConfigError) as err:
            validation_service.validate_config_is_not_empty(mock_config)

        # assert
        error_message = "Missing required values from config: ['database_password']"
        assert err.value.args[0] == error_message
        assert (
                   "root",
                   40,
                   error_message,
               ) in caplog.record_tuples

    def test_validate_request_values_are_not_empty_does_not_raise_an_exception_when_given_valid_request(
            self,
    ):
        # arrange
        validation_service = ValidationService()
        mock_request = flask.Request.from_values(
            json={"questionnaire_name": "test_questionnaire_name"}
        )

        # act

        # assert
        with does_not_raise(RequestError):
            validation_service.validate_request_values_are_not_empty(
                mock_request
            )

    @pytest.mark.parametrize(
        "questionnaire_name",
        [None, ""],
    )
    def test_validate_request_values_are_not_empty_logs_and_raises_request_error_when_questionnaire_name_is_missing(
            self, questionnaire_name, caplog
    ):
        # arrange
        validation_service = ValidationService()
        mock_request = flask.Request.from_values(
            json={"questionnaire_name": questionnaire_name}
        )

        # act
        with pytest.raises(RequestError) as err:
            validation_service.validate_request_values_are_not_empty(mock_request)

        # assert
        error_message = "Missing required values from request: ['questionnaire_name']"
        assert err.value.args[0] == error_message
        assert (
                   "root",
                   40,
                   error_message,
               ) in caplog.record_tuples
