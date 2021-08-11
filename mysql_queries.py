import mysql.connector

class MySQLQueries:
    def __init__(self, user, password, host, database, raise_on_warnings, use_pure):
        self.user = user
        self.password = password
        self.host = host
        self.database = database
        self.raise_on_warnings = raise_on_warnings
        self.use_pure = use_pure

    def connect_db(self):
        config = {
            'user': self.user,
            'password': self.password,
            'host': self.host,
            'database': self.database,
            'raise_on_warnings': self.raise_on_warnings,
            'use_pure': self.use_pure
        }
        cnx = mysql.connector.connect(**config)
        return cnx

    def mysql_query(self, query):
        cnx = self.connect_db()
        cursor = cnx.cursor()
        query = query
        cursor.execute(query)
        row = cursor.fetchall()
        cursor.close()
        cnx.close()
        return row


    def mysql_insert_data(self, query, insert_data):
        cnx = self.connect_db()
        cursor = cnx.cursor()
        query = query
        cursor.execute(query, insert_data)
        cnx.commit()
        cursor.close()
        cnx.close()


