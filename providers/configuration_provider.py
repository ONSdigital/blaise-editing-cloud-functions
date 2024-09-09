from google.cloud.sql.connector import IPTypes

from appconfig.sql_configuration import SqlConfiguration
from models.database_connection_model import DatabaseConnectionModel
from services.validation_service import ValidationService


class ConfigurationProvider:
    def __init__(self, validation_service: ValidationService, sql_configuration: SqlConfiguration) -> None:
        self._validation_service = validation_service
        self._sql_configuration = sql_configuration

    def get_database_connection_model(self) -> DatabaseConnectionModel:
        sql_config = self._sql_configuration.from_env()
        self._validation_service.validate_config(sql_config)

        return DatabaseConnectionModel(
            instance_name=sql_config.instance_name,
            database_name="blaise",
            database_driver="pymysql",
            database_url="mysql+pymysql://",
            database_username=sql_config.database_username,
            database_password=sql_config.database_password,
            database_ip_connection_type=IPTypes.PUBLIC
        )
