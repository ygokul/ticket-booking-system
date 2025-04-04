import mysql.connector

class DBUtil:
    @staticmethod
    def getDBConn():
        return mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="root",
            database="ticketbookingsystem",
            port=3306
        )
