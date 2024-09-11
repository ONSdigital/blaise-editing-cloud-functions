import logging

import flask

from factories.service_instance_factory import ServiceInstanceFactory
from utilities.custom_exceptions import ConfigError
from utilities.logging import setup_logger

setup_logger()


def copy_cases_to_unedited(request: flask.request) -> tuple[str, int]:
    try:
        logging.info("Running Cloud Function - 'copy_cases_to_unedited'")

        request_json = request.get_json()

        questionnaire_name = request_json["questionnaire_name"]
        if questionnaire_name is None or questionnaire_name == "":
            raise ValueError("Missing required fields: 'questionnaire_name'")

        case_service = ServiceInstanceFactory.create_case_service()
        case_service.copy_cases(questionnaire_name)

        logging.info("Finished Running Cloud Function - 'copy_cases_to_unedited'")
        return f"Successfully copied cases to unedited", 200
    except (ConfigError, ValueError) as e:
        error_message = f"Error copying cases to unedited: {e}"
        logging.error(error_message)
        return error_message, 400
