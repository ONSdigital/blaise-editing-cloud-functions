from unittest.mock import call, patch
import pytest
import sqlalchemy
from google.cloud.sql.connector import Connector, IPTypes

from appconfig.sql_configuration import SqlConfiguration
from models.database_connection_model import DatabaseConnectionModel
from providers.configuration_provider import ConfigurationProvider
from services.database_connection_service import DatabaseConnectionService
from services.validation_service import ValidationService
from tests.helper import get_default_config


class TestDatabaseConnectionFunctionality:

    @pytest.fixture()
    def validation_service(self) -> ValidationService:
        return ValidationService()

    @pytest.fixture()
    def sql_config(self) -> SqlConfiguration:
        return get_default_config()

    @pytest.fixture()
    def connection_model(self, sql_config) -> DatabaseConnectionModel:
        return DatabaseConnectionModel(
            instance_name=sql_config.instance_name,
            database_name="blaise",
            database_driver="pymysql",
            database_url="mysql+pymysql://",
            database_username=sql_config.database_username,
            database_password=sql_config.database_password,
            database_ip_connection_type=IPTypes.PUBLIC
        )

    @pytest.fixture()
    def configuration_provider(self, validation_service, sql_config) -> ConfigurationProvider:
        return ConfigurationProvider(validation_service, sql_config)

    @pytest.fixture()
    def service_under_test(self, configuration_provider) -> DatabaseConnectionService:
        return DatabaseConnectionService(configuration_provider)

    @patch.object(Connector, 'connect')
    def test_get_connector_uses_the_connection_model_to_connect_to_the_database(self,
                                                                                mock_connector,
                                                                                service_under_test,
                                                                                sql_config,
                                                                                connection_model):
        # arrange

        # act
        service_under_test.get_connector()

        # assert
        mock_connector.assert_has_calls(
            [call(instance_connection_string=connection_model.instance_name,
                  driver=connection_model.database_driver,
                  user=connection_model.database_username,
                  password=connection_model.database_password,
                  db=connection_model.database_name)],
            any_order=True)

    @patch.object(Connector, 'connect')
    @patch.object(sqlalchemy, 'create_engine')
    def test_get_database_uses_the_connection_model_database_url_and_connector_to_create_an_engine(self,
                                                                                                   mock_engine,
                                                                                                   mock_connector,
                                                                                                   service_under_test,
                                                                                                   connection_model):
        # arrange

        # act
        service_under_test.get_database()

        # assert
        mock_engine.assert_has_calls(
            [call(url=connection_model.database_url, creator=mock_connector(), pool_pre_ping=True)])

