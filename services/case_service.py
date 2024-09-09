import logging

from providers.configuration_provider import ConfigurationProvider

class CaseService:
    def __init__(self, configuration_provider: ConfigurationProvider) -> None:
        self._configuration_provider = configuration_provider

    def copy_cases(self, source_table: str, destination_table: str) -> tuple[str, int]:
        try:
            logging.info("Running Cloud Function - 'copy_cases_to_unedited'")

            connection_model = self._configuration_provider.get_database_connection_model()




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
