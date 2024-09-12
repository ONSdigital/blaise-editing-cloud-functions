import os

from google.cloud.sql.connector import IPTypes

from models.database_connection_model import DatabaseConnectionModel
from utilities.custom_exceptions import ConfigError


class ConfigurationProvider:

    def get_database_connection_model(self) -> DatabaseConnectionModel:
        return DatabaseConnectionModel(
            instance_name=self.build_instance_name(),
            database_name="blaise",
            database_driver="pymysql",
            database_url="mysql+pymysql://",
            database_username=self.get_environment_variable("DATABASE_USERNAME"),
            database_password=self.get_environment_variable("DATABASE_PASSWORD"),
            database_ip_connection_type=IPTypes.PUBLIC
        )

    def build_instance_name(self) -> str:
        project_name = self.get_environment_variable("PROJECT_ID")
        region = self.get_environment_variable("REGION")
        db_instance_name = self.get_environment_variable("INSTANCE_NAME")
        return f"{project_name}:{region}:{db_instance_name}"

    @staticmethod
    def get_environment_variable(variable_name: str) -> str:
        environment_variable = os.getenv(variable_name, None)
        if environment_variable is None or environment_variable == "":
            raise ConfigError(f"Missing environment variable: {variable_name}")
        return environment_variable
