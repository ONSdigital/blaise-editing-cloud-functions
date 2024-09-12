import logging

import flask

from utilities.custom_exceptions import (
    ConfigError, RequestError,
)


class ValidationService:
    def __init__(self) -> None:
        self.request_json = None

    @staticmethod
    def validate_config_is_not_empty(config):
        missing_configs = []
        if config.instance_name is None or config.instance_name == "":
            missing_configs.append("instance_name")
        if config.database_username is None or config.database_username == "":
            missing_configs.append("database_username")
        if config.database_password is None or config.database_password == "":
            missing_configs.append("database_password")

        if missing_configs:
            error_message = f"Missing required values from config: {missing_configs}"
            logging.error(error_message)
            raise ConfigError(error_message)

    @staticmethod
    def validate_request_values_are_not_empty(request: flask.request):
        missing_values = []
        questionnaire_name = request.json["questionnaire_name"]
        if questionnaire_name is None or questionnaire_name == "":
            missing_values.append("questionnaire_name")

        if missing_values:
            error_message = f"Missing required values from request: {missing_values}"
            logging.error(error_message)
            raise RequestError(error_message)
