from unittest.mock import call, patch, Mock
import pytest
import sqlalchemy
from google.cloud.sql.connector import Connector, IPTypes

from models.database_connection_model import DatabaseConnectionModel
from providers.configuration_provider import ConfigurationProvider
from services.database_connection_service import DatabaseConnectionService


class TestDatabaseConnectionFunctionality:

    @pytest.fixture()
    def connection_model(self) -> DatabaseConnectionModel:
        return DatabaseConnectionModel(
            instance_name="test:test:test",
            database_name="blaise",
            database_driver="pymysql",
            database_url="mysql+pymysql://",
            database_username="test_user",
            database_password="test_password",
            database_ip_connection_type=IPTypes.PUBLIC
        )

    @pytest.fixture()
    def mock_configuration_provider(self):
        return Mock()

    @pytest.fixture()
    def service_under_test(self, mock_configuration_provider, connection_model) -> DatabaseConnectionService:
        mock_configuration_provider.get_database_connection_model.return_value = connection_model
        return DatabaseConnectionService(mock_configuration_provider)

    @patch.object(Connector, 'connect')
    def test_get_connector_uses_the_connection_model_to_connect_to_the_database(self,
                                                                                mock_connector,
                                                                                service_under_test,
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

