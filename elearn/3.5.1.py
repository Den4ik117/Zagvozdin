import sqlite3
import pandas as pd

DATABASE = '../database/currency_value.db'
PATH_TO_INPUT_FILE = '../data/currency_value.csv'
TABLE_NAME = 'currency_value'

class CSV2SQL:
    """Класс для преобразования CSV-таблицы в базу данных SQLite
    """
    @staticmethod
    def convert():
        """Метод создаёт базу данных на основе CSV-файла
        """
        con = sqlite3.connect(DATABASE)
        df = pd.read_csv(PATH_TO_INPUT_FILE)
        df.to_sql(name=TABLE_NAME, con=con)


if __name__ == '__main__':
    CSV2SQL.convert()