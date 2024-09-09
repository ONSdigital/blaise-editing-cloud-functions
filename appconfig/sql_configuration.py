import os
from dataclasses import dataclass


@dataclass
class SqlConfiguration:
    instance_name: str
    database_username: str
    database_password: str

    @classmethod
    def from_env(cls):
        return cls(
            instance_name=os.getenv("INSTANCE_NAME"),
            database_username=os.getenv("DATABASE_USERNAME"),
            database_password=os.getenv("DATABASE_PASSWORD")
        )