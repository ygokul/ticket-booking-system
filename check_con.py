from util.db_conn_util import DBConnUtil
from util.db_property_util import DBPropertyUtil

conn_str = DBPropertyUtil.get_connection_string("db.properties")
conn = DBConnUtil.get_connection(conn_str)

if conn:
    print("Successfully connected to MySQL database!")
    conn.close()
else:
    print("Connection failed")