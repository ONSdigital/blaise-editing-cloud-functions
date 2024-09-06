import logging

from appconfig.config import Config
from utilities.custom_exceptions import ConfigError
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

        logging.info("Finished Running Cloud Function - 'copy_cases_to_unedited'")
        return f"Successfully copied cases to unedited", 200
    except ConfigError as e:
        error_message = f"Error copying cases to unedited: {e}"
        logging.error(error_message)
        return error_message, 400
