from contextlib import contextmanager

import pytest
from google.cloud.sql.connector import IPTypes

from models.database_connection_model import DatabaseConnectionModel
from providers.configuration_provider import ConfigurationProvider
from utilities.custom_exceptions import ConfigError


@contextmanager
def does_not_raise(expected_exception):
    try:
        yield

    except expected_exception as error:
        raise AssertionError(f"Raised exception {error} when it should not!")

    except Exception as error:
        raise AssertionError(f"An unexpected exception {error} raised.")


class TestConfigurationProvider:

    @pytest.fixture
    def service_under_test(self) -> ConfigurationProvider:
        return ConfigurationProvider()

    def test_get_database_connection_model_returns_expected_result_with_valid_environment_variables(self,
                                                                                                    monkeypatch,
                                                                                                    service_under_test):
        # arrange
        monkeypatch.setenv('PROJECT_ID', 'test_project_id')
        monkeypatch.setenv('REGION', 'test_region')
        monkeypatch.setenv('INSTANCE_NAME', 'test_instance_name')
        monkeypatch.setenv('DATABASE_USERNAME', 'test_database_username')
        monkeypatch.setenv('DATABASE_PASSWORD', 'test_database_password')

        expected_result = DatabaseConnectionModel(
            instance_name="test_project_id:test_region:test_instance_name",
            database_name="blaise",
            database_driver="pymysql",
            database_url="mysql+pymysql://",
            database_username="test_database_username",
            database_password="test_database_password",
            database_ip_connection_type=IPTypes.PUBLIC)

        # act
        actual_result = service_under_test.get_database_connection_model()

        # assert
        assert expected_result.instance_name == actual_result.instance_name
        assert expected_result.database_name == actual_result.database_name
        assert expected_result.database_driver == actual_result.database_driver
        assert expected_result.database_url == actual_result.database_url
        assert expected_result.database_username == actual_result.database_username
        assert expected_result.database_password == actual_result.database_password
        assert expected_result.database_ip_connection_type == actual_result.database_ip_connection_type

    def test_get_database_connection_model_does_not_error_with_valid_environment_variables(self,
                                                                                           monkeypatch,
                                                                                           service_under_test):
        # arrange
        monkeypatch.setenv('PROJECT_ID', 'test_project_id')
        monkeypatch.setenv('REGION', 'test_region')
        monkeypatch.setenv('INSTANCE_NAME', 'test_instance_name')
        monkeypatch.setenv('DATABASE_USERNAME', 'test_database_username')
        monkeypatch.setenv('DATABASE_PASSWORD', 'test_database_password')

        # assert
        with does_not_raise(ConfigError):
            service_under_test.get_database_connection_model()

    def test_get_database_connection_model_raises_config_error_with_project_id_not_set(self,
                                                                                       monkeypatch,
                                                                                       service_under_test):
        # arrange
        monkeypatch.setenv('REGION', 'test_region')
        monkeypatch.setenv('INSTANCE_NAME', 'test_instance_name')
        monkeypatch.setenv('DATABASE_USERNAME', 'test_database_username')
        monkeypatch.setenv('DATABASE_PASSWORD', 'test_database_password')

        # act
        with pytest.raises(ConfigError) as err:
            service_under_test.get_database_connection_model()

        # assert
        error_message = "Missing environment variable: PROJECT_ID"
        assert err.value.args[0] == error_message

    def test_get_database_connection_model_raises_config_error_when_project_id_empty(self,
                                                                                     monkeypatch,
                                                                                     service_under_test):
        # arrange
        monkeypatch.setenv('PROJECT_ID', '')
        monkeypatch.setenv('REGION', 'test_region')
        monkeypatch.setenv('INSTANCE_NAME', 'test_instance_name')
        monkeypatch.setenv('DATABASE_USERNAME', 'test_database_username')
        monkeypatch.setenv('DATABASE_PASSWORD', 'test_database_password')

        # act
        with pytest.raises(ConfigError) as err:
            service_under_test.get_database_connection_model()

        # assert
        error_message = "Missing environment variable: PROJECT_ID"
        assert err.value.args[0] == error_message

    def test_get_database_connection_model_raises_config_error_with_region_not_set(self,
                                                                                   monkeypatch,
                                                                                   service_under_test):
        # arrange
        monkeypatch.setenv('PROJECT_ID', 'test_project_id')
        monkeypatch.setenv('INSTANCE_NAME', 'test_instance_name')
        monkeypatch.setenv('DATABASE_USERNAME', 'test_database_username')
        monkeypatch.setenv('DATABASE_PASSWORD', 'test_database_password')

        # act
        with pytest.raises(ConfigError) as err:
            service_under_test.get_database_connection_model()

        # assert
        error_message = "Missing environment variable: REGION"
        assert err.value.args[0] == error_message

    def test_get_database_connection_model_raises_config_error_when_region_is_empty(self,
                                                                                    monkeypatch,
                                                                                    service_under_test):
        # arrange
        monkeypatch.setenv('PROJECT_ID', 'test_project_id')
        monkeypatch.setenv('REGION', '')
        monkeypatch.setenv('INSTANCE_NAME', 'test_instance_name')
        monkeypatch.setenv('DATABASE_USERNAME', 'test_database_username')
        monkeypatch.setenv('DATABASE_PASSWORD', 'test_database_password')

        # act
        with pytest.raises(ConfigError) as err:
            service_under_test.get_database_connection_model()

        # assert
        error_message = "Missing environment variable: REGION"
        assert err.value.args[0] == error_message

    def test_get_database_connection_model_raises_config_error_with_instance_name_not_set(self,
                                                                                          monkeypatch,
                                                                                          service_under_test):
        # arrange
        monkeypatch.setenv('PROJECT_ID', 'test_project_id')
        monkeypatch.setenv('REGION', 'test_region')
        monkeypatch.setenv('DATABASE_USERNAME', 'test_database_username')
        monkeypatch.setenv('DATABASE_PASSWORD', 'test_database_password')

        # act
        with pytest.raises(ConfigError) as err:
            service_under_test.get_database_connection_model()

        # assert
        error_message = "Missing environment variable: INSTANCE_NAME"
        assert err.value.args[0] == error_message

    def test_get_database_connection_model_raises_config_error_when_instance_name_is_empty(self,
                                                                                           monkeypatch,
                                                                                           service_under_test):
        # arrange
        monkeypatch.setenv('PROJECT_ID', 'test_project_id')
        monkeypatch.setenv('REGION', 'test_region')
        monkeypatch.setenv('INSTANCE_NAME', '')
        monkeypatch.setenv('DATABASE_USERNAME', 'test_database_username')
        monkeypatch.setenv('DATABASE_PASSWORD', 'test_database_password')

        # act
        with pytest.raises(ConfigError) as err:
            service_under_test.get_database_connection_model()

        # assert
        error_message = "Missing environment variable: INSTANCE_NAME"
        assert err.value.args[0] == error_message

    def test_get_database_connection_model_raises_config_error_with_database_username_not_set(self,
                                                                                              monkeypatch,
                                                                                              service_under_test):
        # arrange
        monkeypatch.setenv('PROJECT_ID', 'test_project_id')
        monkeypatch.setenv('REGION', 'test_region')
        monkeypatch.setenv('INSTANCE_NAME', 'test_instance_name')
        monkeypatch.setenv('DATABASE_PASSWORD', 'test_database_password')

        # act
        with pytest.raises(ConfigError) as err:
            service_under_test.get_database_connection_model()

        # assert
        error_message = "Missing environment variable: DATABASE_USERNAME"
        assert err.value.args[0] == error_message

    def test_get_database_connection_model_raises_config_error_when_database_username_is_empty(self,
                                                                                               monkeypatch,
                                                                                               service_under_test):
        # arrange
        monkeypatch.setenv('PROJECT_ID', 'test_project_id')
        monkeypatch.setenv('REGION', 'test_region')
        monkeypatch.setenv('INSTANCE_NAME', 'test_instance_name')
        monkeypatch.setenv('DATABASE_USERNAME', '')
        monkeypatch.setenv('DATABASE_PASSWORD', 'test_database_password')

        # act
        with pytest.raises(ConfigError) as err:
            service_under_test.get_database_connection_model()

        # assert
        error_message = "Missing environment variable: DATABASE_USERNAME"
        assert err.value.args[0] == error_message

    def test_get_database_connection_model_raises_config_error_with_database_password_not_set(self,
                                                                                              monkeypatch,
                                                                                              service_under_test):
        # arrange
        monkeypatch.setenv('PROJECT_ID', 'test_project_id')
        monkeypatch.setenv('REGION', 'test_region')
        monkeypatch.setenv('INSTANCE_NAME', 'test_instance_name')
        monkeypatch.setenv('DATABASE_USERNAME', 'test_database_username')

        # act
        with pytest.raises(ConfigError) as err:
            service_under_test.get_database_connection_model()

        # assert
        error_message = "Missing environment variable: DATABASE_PASSWORD"
        assert err.value.args[0] == error_message

    def test_get_database_connection_model_raises_config_error_when_database_password_is_empty(self,
                                                                                              monkeypatch,
                                                                                              service_under_test):
        # arrange
        monkeypatch.setenv('PROJECT_ID', 'test_project_id')
        monkeypatch.setenv('REGION', 'test_region')
        monkeypatch.setenv('INSTANCE_NAME', 'test_instance_name')
        monkeypatch.setenv('DATABASE_USERNAME', 'test_database_username')
        monkeypatch.setenv('DATABASE_PASSWORD', '')

        # act
        with pytest.raises(ConfigError) as err:
            service_under_test.get_database_connection_model()

        # assert
        error_message = "Missing environment variable: DATABASE_PASSWORD"
        assert err.value.args[0] == error_message
