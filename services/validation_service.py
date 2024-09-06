import logging

from utilities.custom_exceptions import (
    ConfigError,
)


class ValidationService:
    def __init__(self) -> None:
        self.request_json = None

    @staticmethod
    def validate_config(config):
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
