import mysql.connector
from util.db_property_util import DBPropertyUtil
from mysql.connector import Error

class DBConnUtil:
    @staticmethod
    def get_connection(connection_string: str):
        try:
            # Parse the connection string
            params = dict(param.split('=') for param in connection_string.split())
            
            conn = mysql.connector.connect(
                host=params.get('host'),
                database=params.get('dbname'),
                user=params.get('user'),
                password=params.get('password')
            )
            return conn
        except Error as e:
            print(f"Error connecting to database: {e}")
            return None