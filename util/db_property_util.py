import configparser
import os

class DBPropertyUtil:
    @staticmethod
    def get_connection_string(property_file_name: str) -> str:
        if not os.path.exists(property_file_name):
            raise FileNotFoundError(f"Property file '{property_file_name}' not found")
        
        config = configparser.ConfigParser()
        config.read(property_file_name)
        
        if 'database' not in config:
            raise ValueError("Database section not found in property file")
        
        db_config = config['database']
        required_keys = ['host', 'database', 'user', 'password']
        
        for key in required_keys:
            if key not in db_config:
                raise ValueError(f"Missing required database configuration: {key}")
        
        # Format for MySQL connection string
        return f"host={db_config['host']} dbname={db_config['database']} user={db_config['user']} password={db_config['password']}"