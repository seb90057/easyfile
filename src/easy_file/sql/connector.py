import sqlite3
from sqlite3 import Error


class SqlConnector:

    conn = None
    db_file = r"C:\sqlite_db\easy_file.db"

    @staticmethod
    def get_or_create_connection():
        """
        Create a connection to db_file
        :param db_file: path to db
        :return: the connection
        """
        if not SqlConnector.conn:
            try:
                SqlConnector.conn = sqlite3.connect(SqlConnector.db_file)
                print(sqlite3.version)
            except Error as e:
                print(e)
        return SqlConnector.conn

    @staticmethod
    def execute_request(request):
        conn = SqlConnector.get_or_create_connection()
        try:
            c = conn.cursor()
            c.execute(request)
            SqlConnector.commit()
            return [h[0] for h in c.description], c.fetchall()
        except Error as e:
            print(e)
        return None

    @staticmethod
    def commit():
        SqlConnector.conn.commit()

    @staticmethod
    def get_table_list():
        request = "SELECT name FROM sqlite_master WHERE type ='table' AND name NOT LIKE 'sqlite_%';"
        _, tables = SqlConnector.execute_request(request)
        return [table[0] for table in tables]


if __name__ == '__main__':
    # SqlConnector.get_or_create_connection()
    res = SqlConnector.get_table_list()
    print(res)