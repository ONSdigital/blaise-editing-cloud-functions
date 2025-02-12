class DatabaseConnectionModel:

    def __init__(
        self,
        database_name: str,
        database_username: str,
        database_password: str,
        database_ip_address: str,
        database_port: int,
    ):
        self.database_name = database_name
        self.database_username = database_username
        self.database_password = database_password
        self.database_ip_address = database_ip_address
        self.database_port = database_port
