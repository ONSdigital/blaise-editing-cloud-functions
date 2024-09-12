from contextlib import contextmanager

import flask
import pytest

from services.validation_service import ValidationService
from utilities.custom_exceptions import (
    RequestError,
)


@contextmanager
def does_not_raise(expected_exception):
    try:
        yield

    except expected_exception as error:
        raise AssertionError(f"Raised exception {error} when it should not!")

    except Exception as error:
        raise AssertionError(f"An unexpected exception {error} raised.")


class MockRequest:
    def __init__(self, json_data):
        self.json_data = json_data

    def get_json(self):
        return self.json_data


class TestValidationService:

    def test_validate_request_values_are_not_empty_does_not_raise_an_exception_when_given_valid_request(
            self,
    ):
        # arrange
        validation_service = ValidationService()
        mock_request = flask.Request.from_values(
            json={"questionnaire_name": "test_questionnaire_name"}
        )

        # act

        # assert
        with does_not_raise(RequestError):
            validation_service.validate_request_values_are_not_empty(
                mock_request
            )

    @pytest.mark.parametrize(
        "questionnaire_name",
        [None, ""],
    )
    def test_validate_request_values_are_not_empty_logs_and_raises_request_error_when_questionnaire_name_is_missing(
            self, questionnaire_name, caplog
    ):
        # arrange
        validation_service = ValidationService()
        mock_request = flask.Request.from_values(
            json={"questionnaire_name": questionnaire_name}
        )

        # act
        with pytest.raises(RequestError) as err:
            validation_service.validate_request_values_are_not_empty(mock_request)

        # assert
        error_message = "Missing required values from request: ['questionnaire_name']"
        assert err.value.args[0] == error_message
        assert (
                   "root",
                   40,
                   error_message,
               ) in caplog.record_tuples
