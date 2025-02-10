from contextlib import contextmanager

import pytest

from models.blaise_connection_model import BlaiseConnectionModel
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
        monkeypatch.setenv('DATABASE_NAME', 'test_database_name')
        monkeypatch.setenv('DATABASE_IP_ADDRESS', '0.0.0.0')
        monkeypatch.setenv('DATABASE_USERNAME', 'test_database_username')
        monkeypatch.setenv('DATABASE_PASSWORD', 'test_database_password')
        monkeypatch.setenv('DATABASE_PORT', '1234')

        expected_result = DatabaseConnectionModel(
            database_ip_address="0.0.0.0",
            database_name="test_database_name",
            database_username="test_database_username",
            database_password="test_database_password",
            database_port=1234
        )

        # act
        actual_result = service_under_test.get_database_connection_model()

        # assert
        assert expected_result.database_ip_address == actual_result.database_ip_address
        assert expected_result.database_name == actual_result.database_name
        assert expected_result.database_username == actual_result.database_username
        assert expected_result.database_password == actual_result.database_password
        assert expected_result.database_port == actual_result.database_port

    def test_get_database_connection_model_does_not_error_with_valid_environment_variables(self,
                                                                                           monkeypatch,
                                                                                           service_under_test):
        # arrange
        monkeypatch.setenv('DATABASE_NAME', 'test_database_name')
        monkeypatch.setenv('DATABASE_IP_ADDRESS', '0.0.0.0')
        monkeypatch.setenv('DATABASE_USERNAME', 'test_database_username')
        monkeypatch.setenv('DATABASE_PASSWORD', 'test_database_password')
        monkeypatch.setenv('DATABASE_PORT', '1234')

        # assert
        with does_not_raise(ConfigError):
            service_under_test.get_database_connection_model()

    def test_get_database_connection_model_raises_config_error_with_database_ip_address_not_set(self,
                                                                                                monkeypatch,
                                                                                                service_under_test):
        # arrange
        monkeypatch.setenv('DATABASE_NAME', 'test_database_name')
        monkeypatch.setenv('DATABASE_USERNAME', 'test_database_username')
        monkeypatch.setenv('DATABASE_PASSWORD', 'test_database_password')
        monkeypatch.setenv('DATABASE_PORT', '1234')

        # act
        with pytest.raises(ConfigError) as err:
            service_under_test.get_database_connection_model()

        # assert
        error_message = "Missing environment variable: DATABASE_IP_ADDRESS"
        assert err.value.args[0] == error_message

    def test_get_database_connection_model_raises_config_error_when_database_ip_address_empty(self,
                                                                                              monkeypatch,
                                                                                              service_under_test):
        # arrange
        monkeypatch.setenv('DATABASE_NAME', 'test_database_name')
        monkeypatch.setenv('DATABASE_IP_ADDRESS', '')
        monkeypatch.setenv('DATABASE_USERNAME', 'test_database_username')
        monkeypatch.setenv('DATABASE_PASSWORD', 'test_database_password')
        monkeypatch.setenv('DATABASE_PORT', '1234')

        # act
        with pytest.raises(ConfigError) as err:
            service_under_test.get_database_connection_model()

        # assert
        error_message = "Missing environment variable: DATABASE_IP_ADDRESS"
        assert err.value.args[0] == error_message

    def test_get_database_connection_model_raises_config_error_with_database_username_not_set(self,
                                                                                              monkeypatch,
                                                                                              service_under_test):
        # arrange
        monkeypatch.setenv('DATABASE_NAME', 'test_database_name')
        monkeypatch.setenv('DATABASE_IP_ADDRESS', '0.0.0.0')
        monkeypatch.setenv('DATABASE_PASSWORD', 'test_database_password')
        monkeypatch.setenv('DATABASE_PORT', '1234')

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
        monkeypatch.setenv('DATABASE_NAME', 'test_database_name')
        monkeypatch.setenv('DATABASE_IP_ADDRESS', '0.0.0.0')
        monkeypatch.setenv('DATABASE_USERNAME', '')
        monkeypatch.setenv('DATABASE_PASSWORD', 'test_database_password')
        monkeypatch.setenv('DATABASE_PORT', '1234')

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
        monkeypatch.setenv('DATABASE_NAME', 'test_database_name')
        monkeypatch.setenv('DATABASE_IP_ADDRESS', '0.0.0.0')
        monkeypatch.setenv('DATABASE_USERNAME', 'test_database_username')
        monkeypatch.setenv('DATABASE_PORT', '1234')

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
        monkeypatch.setenv('DATABASE_NAME', 'test_database_name')
        monkeypatch.setenv('DATABASE_IP_ADDRESS', '0.0.0.0')
        monkeypatch.setenv('DATABASE_USERNAME', 'test_database_username')
        monkeypatch.setenv('DATABASE_PASSWORD', '')
        monkeypatch.setenv('DATABASE_PORT', '1234')

        # act
        with pytest.raises(ConfigError) as err:
            service_under_test.get_database_connection_model()

        # assert
        error_message = "Missing environment variable: DATABASE_PASSWORD"
        assert err.value.args[0] == error_message

    def test_get_database_connection_model_raises_config_error_with_database_name_not_set(self,
                                                                                          monkeypatch,
                                                                                          service_under_test):
        # arrange
        monkeypatch.setenv('DATABASE_IP_ADDRESS', '0.0.0.0')
        monkeypatch.setenv('DATABASE_USERNAME', 'test_database_username')
        monkeypatch.setenv('DATABASE_PASSWORD', 'test_database_password')
        monkeypatch.setenv('DATABASE_PORT', '1234')

        # act
        with pytest.raises(ConfigError) as err:
            service_under_test.get_database_connection_model()

        # assert
        error_message = "Missing environment variable: DATABASE_NAME"
        assert err.value.args[0] == error_message

    def test_get_database_connection_model_raises_config_error_when_database_name_is_empty(self,
                                                                                           monkeypatch,
                                                                                           service_under_test):
        # arrange
        monkeypatch.setenv('DATABASE_NAME', '')
        monkeypatch.setenv('DATABASE_IP_ADDRESS', '0.0.0.0')
        monkeypatch.setenv('DATABASE_USERNAME', 'test_database_username')
        monkeypatch.setenv('DATABASE_PASSWORD', 'test_database_password')
        monkeypatch.setenv('DATABASE_PORT', '1234')

        # act
        with pytest.raises(ConfigError) as err:
            service_under_test.get_database_connection_model()

        # assert
        error_message = "Missing environment variable: DATABASE_NAME"
        assert err.value.args[0] == error_message

    def test_get_database_connection_model_raises_config_error_with_database_port_not_set(self,
                                                                                          monkeypatch,
                                                                                          service_under_test):
        # arrange
        monkeypatch.setenv('DATABASE_NAME', 'test_database_name')
        monkeypatch.setenv('DATABASE_IP_ADDRESS', '0.0.0.0')
        monkeypatch.setenv('DATABASE_USERNAME', 'test_database_username')
        monkeypatch.setenv('DATABASE_PASSWORD', 'test_database_password')

        # act
        with pytest.raises(ConfigError) as err:
            service_under_test.get_database_connection_model()

        # assert
        error_message = "Missing environment variable: DATABASE_PORT"
        assert err.value.args[0] == error_message

    def test_get_database_connection_model_raises_config_error_when_database_port_is_empty(self,
                                                                                           monkeypatch,
                                                                                           service_under_test):
        # arrange
        monkeypatch.setenv('DATABASE_NAME', 'test_database_name')
        monkeypatch.setenv('DATABASE_IP_ADDRESS', '0.0.0.0')
        monkeypatch.setenv('DATABASE_USERNAME', 'test_database_username')
        monkeypatch.setenv('DATABASE_PASSWORD', 'test_database_password')
        monkeypatch.setenv('DATABASE_PORT', '')

        # act
        with pytest.raises(ConfigError) as err:
            service_under_test.get_database_connection_model()

        # assert
        error_message = "Missing environment variable: DATABASE_PORT"
        assert err.value.args[0] == error_message

    def test_get_database_connection_model_raises_config_error_when_database_port_is_not_a_number(self,
                                                                                                  monkeypatch,
                                                                                                  service_under_test):
        # arrange
        monkeypatch.setenv('DATABASE_NAME', 'test_database_name')
        monkeypatch.setenv('DATABASE_IP_ADDRESS', '0.0.0.0')
        monkeypatch.setenv('DATABASE_USERNAME', 'test_database_username')
        monkeypatch.setenv('DATABASE_PASSWORD', 'test_database_password')
        monkeypatch.setenv('DATABASE_PORT', 'test')

        # act
        with pytest.raises(ConfigError) as err:
            service_under_test.get_database_connection_model()

        # assert
        error_message = "Environment variable DATABASE_PORT must be a number"
        assert err.value.args[0] == error_message

    def test_get_blaise_connection_model_returns_expected_result_with_valid_environment_variables(self,
                                                                                                  monkeypatch,
                                                                                                  service_under_test):
        # arrange
        monkeypatch.setenv('BLAISE_API_URL', 'testBlaise.com')
        monkeypatch.setenv('BLAISE_SERVER_PARK', 'test_server_park')

        expected_result = BlaiseConnectionModel(
            blaise_api_url="testBlaise.com",
            blaise_server_park="test_server_park"
        )

        # act
        actual_result = service_under_test.get_blaise_connection_model()

        # assert
        assert expected_result.blaise_api_url == actual_result.blaise_api_url
        assert expected_result.blaise_server_park == actual_result.blaise_server_park

    def test_get_blaise_connection_model_does_not_error_with_valid_environment_variables(self,
                                                                                         monkeypatch,
                                                                                         service_under_test):
        # arrange
        monkeypatch.setenv('BLAISE_API_URL', 'testBlaise.com')
        monkeypatch.setenv('BLAISE_SERVER_PARK', 'test_server_park')

        # assert
        with does_not_raise(ConfigError):
            service_under_test.get_blaise_connection_model()

    def test_get_blaise_connection_model_raises_config_error_with_blaise_api_url_not_set(self,
                                                                                         monkeypatch,
                                                                                         service_under_test):
        # arrange
        monkeypatch.setenv('BLAISE_SERVER_PARK', 'test_server_park')

        # act
        with pytest.raises(ConfigError) as err:
            service_under_test.get_blaise_connection_model()

        # assert
        error_message = "Missing environment variable: BLAISE_API_URL"
        assert err.value.args[0] == error_message

    def test_get_blaise_connection_model_raises_config_error_when_blaise_api_url_empty(self,
                                                                                       monkeypatch,
                                                                                       service_under_test):
        # arrange
        monkeypatch.setenv('BLAISE_API_URL', '')
        monkeypatch.setenv('BLAISE_SERVER_PARK', 'test_server_park')

        # act
        with pytest.raises(ConfigError) as err:
            service_under_test.get_blaise_connection_model()

        # assert
        error_message = "Missing environment variable: BLAISE_API_URL"
        assert err.value.args[0] == error_message

    def test_get_blaise_connection_model_raises_config_error_with_blaise_server_park_not_set(self,
                                                                                             monkeypatch,
                                                                                             service_under_test):
        # arrange
        monkeypatch.setenv('BLAISE_API_URL', 'testBlaise.com')

        # act
        with pytest.raises(ConfigError) as err:
            service_under_test.get_blaise_connection_model()

        # assert
        error_message = "Missing environment variable: BLAISE_SERVER_PARK"
        assert err.value.args[0] == error_message

    def test_get_blaise_connection_model_raises_config_error_when_blaise_server_park_empty(self,
                                                                                           monkeypatch,
                                                                                           service_under_test):
        # arrange
        monkeypatch.setenv('BLAISE_API_URL', 'testBlaise.com')
        monkeypatch.setenv('BLAISE_SERVER_PARK', '')

        # act
        with pytest.raises(ConfigError) as err:
            service_under_test.get_blaise_connection_model()

        # assert
        error_message = "Missing environment variable: BLAISE_SERVER_PARK"
        assert err.value.args[0] == error_message
