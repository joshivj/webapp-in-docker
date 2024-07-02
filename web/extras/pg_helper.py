# @todo: refactor this file
class PgHelper:
    def __init__(self, cursor):
        self.cursor = cursor

    def generate_get_all_records_query(self, table_name, columns=None):
        columns_str = '*' if columns is None else ', '.join(columns)
        query = f"SELECT {columns_str} FROM {table_name}"
        return self.cursor.mogrify(query)

    def generate_get_record_query(self, table_name, col_identifier, val_identifier, columns=None):
        columns_str = '*' if columns is None else ', '.join(columns)
        query = f"SELECT {columns_str} FROM {table_name} WHERE {col_identifier}=%s"
        return self.cursor.mogrify(query, [val_identifier])

    def get_all_records(self, table_name, columns):
        query = self.generate_get_all_records_query(table_name, columns)
        self.cursor.execute(query)
        results = self.cursor.fetchall()
        return results if results else []

    def update_record(self):
        pass

    def delete_record(self):
        pass

    def get_record(self, table_name, col_identifier, val_identifier, columns=None):
        query = self.generate_get_record_query(table_name, col_identifier, val_identifier, columns)
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        return result if result else []

