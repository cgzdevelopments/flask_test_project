import psycopg2

class PyPostgreSQL:
    def __init__(self, database, user, password, host, port):
        self.database = database
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.connection = None
        self.cursor = None

    def connect(self):
        """Connects to the PostgreSQL database."""
        try:
            self.connection = psycopg2.connect(
                database=self.database,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
            self.cursor = self.connection.cursor()
            print("Connected to PostgreSQL database")
        except Exception as e:
            print(f"Error connecting to database: {e}")
            self.connection = None
            self.cursor = None

    def disconnect(self):
        """Disconnects from the PostgreSQL database."""
        if self.connection:
            self.cursor.close()
            self.connection.close()
            print("Disconnected from PostgreSQL database")

    def raw(self, query, params = None, returning_results=True):
        """Executes a raw SQL query and returns results or row count."""
        if self.cursor is None:
            print("Error: Not connected to the database.")
            return None
        try:
            self.cursor.execute(query, params or ())
            if returning_results:
                columns = [col[0] for col in self.cursor.description]
                results = []
                for row in self.cursor.fetchall():
                    results.append(dict(zip(columns, row)))
                return results
            else:
                self.connection.commit()
                return self.cursor.rowcount
        except Exception as e:
            self.connection.rollback()
            print(f"Error executing query: {e}")
            return None