from appconfig.sql_configuration import SqlConfiguration


def get_default_config() -> SqlConfiguration:
    return SqlConfiguration(instance_name="test_instance_name", database_username="test_user",database_password="test_password")
