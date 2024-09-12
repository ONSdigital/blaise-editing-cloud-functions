import logging

import flask

from utilities.custom_exceptions import (
    RequestError,
)


class ValidationService:
    def __init__(self) -> None:
        self.request_json = None

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
