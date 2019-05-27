
import datetime
import mysql.connector


class MySqlCon:
    """Class for submitting queries to the MySQL database.
    """
    def __init__(self):
        """Constructor method for the MySqlCon class.
        Sets up the connection within the cursor object.
        """
        self.config = {
            'host':     'hannl-hlo-bioinformatica-mysqlsrv.mysql.database.azure.com',
            'user':     'owe7_pg7@hannl-hlo-bioinformatica-mysqlsrv.mysql.database.azure.com',
            'password': 'blaat1234',
            'database': 'owe7_pg7'}
        try:
            self.conn = mysql.connector.connect(**self.config)
        except mysql.connector.errors.InterfaceError:
            print(str(datetime.datetime.now()) + "\t\t\tApplication shuts down due to network error")
            raise SystemExit
        self.cursor = self.conn.cursor()

    def execute_res(self, query):
        """Method for executing MySQL queries which return results.
        :param query:(str) query for the MySQL database which returns results.
        :return: rows:(list) list of hits returned from query.
        """
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        return rows

    def execute_no_res(self, query):
        """Method for executing MySQL queries which do not return results.
        :param query:(str) query to be executed in the MySQL database.
        """
        self.cursor.execute(query)

    def close(self):
        """Method for closing the MySQL connection.
        The conn(Connection) object is committed and closed.
        """
        self.conn.commit()
        self.conn.close()
