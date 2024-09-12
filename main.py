import logging

import flask

from factories.service_instance_factory import ServiceInstanceFactory
from utilities.custom_exceptions import ConfigError, RequestError
from utilities.logging import setup_logger

setup_logger()


def copy_cases_to_unedited(request: flask.request) -> tuple[str, int]:
    try:
        logging.info("Running Cloud Function - 'copy_cases_to_unedited'")

        validation_service = ServiceInstanceFactory.create_validation_service()
        validation_service.validate_request_values_are_not_empty(request)

        case_service = ServiceInstanceFactory.create_case_service()
        case_service.copy_cases(request.get_json()["questionnaire_name"])

        logging.info("Finished Running Cloud Function - 'copy_cases_to_unedited'")
        return f"Successfully copied cases to unedited", 200
    except (ConfigError, RequestError) as e:
        error_message = f"Error copying cases to unedited: {e}"
        logging.error(error_message)
        return error_message, 400
    except Exception as e:
        error_message = f"Error copying cases to unedited: {e}"
        logging.error(error_message)
        return error_message, 500
