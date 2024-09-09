from contextlib import contextmanager

import pytest

from appconfig.sql_configuration import Config
from services.validation_service import ValidationService
from tests.helper import get_default_config
from utilities.custom_exceptions import (
    ConfigError,
)


@pytest.fixture()
def config() -> Config:
    return get_default_config()


@contextmanager
def does_not_raise(expected_exception):
    try:
        yield

    except expected_exception as error:
        raise AssertionError(f"Raised exception {error} when it should not!")

    except Exception as error:
        raise AssertionError(f"An unexpected exception {error} raised.")


class TestValidateConfig:
    def test_validate_config_does_not_raise_an_exception_when_given_valid_config(self):
        # arrange
        validation_service = ValidationService()
        mock_config = Config(instance_name="test_instance_name",
                             database_username="test_user",
                             database_password="test_password")

        # assert
        with does_not_raise(ConfigError):
            validation_service.validate_config(mock_config)

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
    def test_validate_config_logs_and_raises_validation_error_exception_when_all_config_values_are_missing(
            self, instance_name, database_username, database_password, caplog
    ):
        # arrange
        mock_config = Config(instance_name=instance_name,
                             database_username=database_username,
                             database_password=database_password)

        validation_service = ValidationService()

        # act
        with pytest.raises(ConfigError) as err:
            validation_service.validate_config(mock_config)

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
    def test_validate_config_logs_and_raises_validation_error_exception_when_instance_name_is_missing(
            self, instance_name, caplog
    ):
        # arrange
        mock_config = Config(instance_name=instance_name,
                             database_username="test_user",
                             database_password="test_password")

        validation_service = ValidationService()

        # act
        with pytest.raises(ConfigError) as err:
            validation_service.validate_config(mock_config)

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
    def test_validate_config_logs_and_raises_validation_error_exception_when_database_username_is_missing(
            self, database_username, caplog
    ):
        # arrange
        mock_config = Config(instance_name="test_instance_name",
                             database_username=database_username,
                             database_password="test_password")

        validation_service = ValidationService()

        # act
        with pytest.raises(ConfigError) as err:
            validation_service.validate_config(mock_config)

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
    def test_validate_config_logs_and_raises_validation_error_exception_when_database_password_is_missing(
            self, database_password, caplog
    ):
        # arrange
        mock_config = Config(instance_name="test_instance_name",
                             database_username="test_user",
                             database_password=database_password)

        validation_service = ValidationService()

        # act
        with pytest.raises(ConfigError) as err:
            validation_service.validate_config(mock_config)

        # assert
        error_message = "Missing required values from config: ['database_password']"
        assert err.value.args[0] == error_message
        assert (
                   "root",
                   40,
                   error_message,
               ) in caplog.record_tuples

