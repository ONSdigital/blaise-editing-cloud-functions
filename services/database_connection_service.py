import sqlalchemy
from google.cloud.sql.connector import Connector
from sqlalchemy import Engine

from providers.configuration_provider import ConfigurationProvider


class DatabaseConnectionService:
    def __init__(self, configuration_provider: ConfigurationProvider):
        self._configuration_provider = configuration_provider
        self._connection_model = self._configuration_provider.get_database_connection_model()

    def get_database(self) -> Engine:
        return sqlalchemy.create_engine(
            url=self._connection_model.database_url,
            creator=self.get_connector(),
            pool_pre_ping=True
        )

    def get_connector(self) -> Connector:
        connector = Connector(self._connection_model.database_ip_connection_type)
        return connector.connect(
            instance_connection_string=self._connection_model.instance_name,
            driver=self._connection_model.database_driver,
            user=self._connection_model.database_username,
            password=self._connection_model.database_password,
            db=self._connection_model.database_name,
        )
