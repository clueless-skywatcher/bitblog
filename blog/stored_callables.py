from django.db import ProgrammingError

class NoDBConnectionError(Exception):
    pass

class FailedInvocation(Exception):
    pass

class StoredFunction:
    def __init__(self, connection, name):
        self.connection = connection
        self.name = name

    def invoke(self, params = []):
        if self.connection is None:
            raise NoDBConnectionError("No database connection was found")
        
        c = self.connection.cursor()

        res = None
        try:
            c.execute(f"SELECT * FROM {self.name}({', '.join([str(p) for p in params])})")
            res = c.fetchall()
        except ProgrammingError:
            raise FailedInvocation("Failed to invoke DB function")
        finally:
            c.close()

        return res