from appconfig.config import Config


def get_default_config() -> Config:
    return Config(instance_name="test_instance_name", database_username="test_user",database_password="test_password")
