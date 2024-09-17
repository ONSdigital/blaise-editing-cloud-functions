import os

from models.database_connection_model import DatabaseConnectionModel
from models.blaise_connection_model import BlaiseConnectionModel
from utilities.custom_exceptions import ConfigError


class ConfigurationProvider:

    def get_database_connection_model(self) -> DatabaseConnectionModel:
        return DatabaseConnectionModel(
            database_name="blaise",
            database_username=self.get_environment_variable("DATABASE_USERNAME"),
            database_password=self.get_environment_variable("DATABASE_PASSWORD"),
            database_ip_address=self.get_environment_variable("DATABASE_IP_ADDRESS"),
            database_port=3306
        )

    def get_blaise_connection_model(self) -> BlaiseConnectionModel:
        return BlaiseConnectionModel(
            blaise_api_url=self.get_environment_variable("BLAISE_API_URL"),
            blaise_server_park=self.get_environment_variable("BLAISE_SERVER_PARK"),
        )

    @staticmethod
    def get_environment_variable(variable_name: str) -> str:
        environment_variable = os.getenv(variable_name, None)
        if environment_variable is None or environment_variable == "":
            raise ConfigError(f"Missing environment variable: {variable_name}")
        return environment_variable
