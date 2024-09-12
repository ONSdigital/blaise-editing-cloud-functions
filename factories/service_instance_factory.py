from appconfig.sql_configuration import SqlConfiguration
from providers.configuration_provider import ConfigurationProvider
from services.case_service import CaseService
from services.database_connection_service import DatabaseConnectionService
from services.validation_service import ValidationService
from services.database_service import DatabaseService


class ServiceInstanceFactory:

    @staticmethod
    def create_validation_service() -> ValidationService:
        return ValidationService()

    @staticmethod
    def create_case_service() -> CaseService:
        validation_service = ValidationService()
        sql_configuration = SqlConfiguration.from_env()
        configuration_provider = ConfigurationProvider(validation_service, sql_configuration)
        database_connection_service = DatabaseConnectionService(configuration_provider)
        database_service = DatabaseService(database_connection_service)
        return CaseService(database_service)

