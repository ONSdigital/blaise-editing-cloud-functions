import logging

from google.cloud.sql.connector import IPTypes

from appconfig.sql_configuration import Config
from models.database_connection_model import DatabaseConnectionModel
from services.database_connection_service import DatabaseConnectionService
from services.database_orm_service import DatabaseOrmService
from utilities.custom_exceptions import ConfigError, OrmError
from utilities.logging import setup_logger
from services.validation_service import ValidationService

setup_logger()


def copy_cases_to_unedited() -> tuple[str, int]:
    try:
        logging.info("Running Cloud Function - 'copy_cases_to_unedited'")
        validation_service = ValidationService()

        # Config Handler
        sql_config = Config.from_env()
        validation_service.validate_config(sql_config)

        connection_model = DatabaseConnectionModel(
            instance_name=sql_config.instance_name,
            database_name="blaise",
            database_driver="pymysql",
            database_url="mysql+pymysql://",
            database_username=sql_config.database_username,
            database_password=sql_config.database_password,
            database_ip_connection_type=IPTypes.PUBLIC
        )

        database = DatabaseConnectionService(connection_model).get_database()
        database_orm_service = DatabaseOrmService()
        table_name = "unedited_table_name"

        if not database_orm_service.check_table_exists(database, table_name):
            logging.info(f"unedited table not found for {table_name}, creating table")

        logging.info("Finished Running Cloud Function - 'copy_cases_to_unedited'")
        return f"Successfully copied cases to unedited", 200
    except (ConfigError, OrmError) as e:
        error_message = f"Error copying cases to unedited: {e}"
        logging.error(error_message)
        return error_message, 400
