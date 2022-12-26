import sqlite3
import pandas as pd
import numpy as np


DATABASE = '../database/currency_value.db'
PATH_TO_INPUT_FILE_1 = '../data/vacancies_dif_currencies.csv'
PATH_TO_INPUT_FILE_2 = '../data/currency_value.csv'
PATH_TO_OUTPUT_FILE = '../data/converted_vacancies_dif_currencies_2.csv'
TABLE_NAME = 'vacancies'


class Converter:
    """Класс для конвертирования в рубли оклада вакансий и
    преобразования столбцов salary_from, salary_to, salary_currency в 1 столбец ― salary

    Attributes:
        source_file (DataFrame): исходная DataFrame-таблица, которую требуется преобразовать
        exchange_rate (DataFrame): DataFrame-таблица, содержащая информацию из ЦентроБанка по стоимость валют с 2003 года
        con (Connection): SQLite Connection с базой данных, по которой мы можем делать запросы
    """

    def __init__(self, file_to_convert, exchange_rate, database):
        """Метод инициализирует класс Converter

        Arguments:
            file_to_convert (str): Файл, который нужно преобразовать
            exchange_rate (str): Файл с валютой из прошлого задания
            database (str): Пусть до базы данных
        """
        self.source_file = pd.read_csv(file_to_convert)
        self.exchange_rate = pd.read_csv(exchange_rate)
        self.con = sqlite3.connect(database)

    def get_converted_dataframe(self, only_head=False):
        """Конвертирует исходный CSV-файл и сохраняет его

        Arguments:
            only_head (bool): Флаг для вывода только первых 100 значений
        """
        df = self.source_file.copy()
        if only_head:
            df = df.head(100)
        df['published_at'] = df['published_at'].apply(lambda x: x[:10])
        df['salary'] = df.apply(lambda x: self.transform_row(x), axis=1)
        df = df[['name', 'salary', 'area_name', 'published_at']]
        df.to_sql(name=TABLE_NAME, con=self.con, if_exists='replace')

    def transform_row(self, row):
        """Преобразует ряд из исходного файла

        Arguments:
            row (Series): ряд таблицы
        """
        salary_from, salary_to, salary_currency = row['salary_from'], row['salary_to'], row['salary_currency']
        if np.isnan(salary_from) and np.isnan(salary_to) or pd.isnull(salary_currency):
            return None
        exchange_value = self.get_converted_salary(row['published_at'], salary_currency)
        if exchange_value is None:
            return None
        salary_from = 0 if np.isnan(salary_from) else salary_from
        salary_to = 0 if np.isnan(salary_to) else salary_to
        result = max(salary_from, salary_to) if salary_to == 0 or salary_from == 0 else ((salary_from + salary_to) / 2)
        return round(result * exchange_value, 0)

    def get_converted_salary(self, date: str, currency: str):
        """Возвращает курс по текущей валюте по указанной дате

        Arguments:
            date (str): дата в формате Y-m
            currency (str): валюта

        Returns:
            int or None: возвращает число, если запись найдена, иначе ― None
        """
        try:
            res = self.con.execute('SELECT {0} FROM `currency_value` WHERE `date` = "{1}"'.format(currency, date[:7])).fetchone()
        except:
            return None
        return res[0] if bool(res) else None


if __name__ == '__main__':
    converter = Converter(PATH_TO_INPUT_FILE_1, PATH_TO_INPUT_FILE_2, DATABASE)
    converter.get_converted_dataframe(only_head=False)
