import pandas as pd
from jinja2 import Environment, FileSystemLoader
import pdfkit


PATH_TO_INPUT_FILE = '../data/converted_vacancies_dif_currencies_full.csv'
TEMPLATES = '../templates'
TEMPLATE = 'template_3_4_2.html'
VACANCY_NAME = 'Дизайнер'


class YearInformation:
    """Класс ― подобие DTO-объекта, который хранит в себе данные об анализе за определённый год

    Attributes:
        salary_average (int): средняя зарплата
        salary_average_for_chosen_vacancy (int): средняя зарплата у выбранной профессии
        vacancy_count (int): количество вакансий
        chosen_vacancy_count (int): количество вакансий у выбранной профессии
        year (int): год
    """
    def __init__(self, df: pd.DataFrame, chosen_vacancy: str, year: int):
        """Метод инициализирует класс YearInformation и высчитывает основные свойства класса

        Params:
            df (DateFrame): исходная таблица с информацией
            chosen_vacancy (str): название выбранной профессии
            year (int): год
        """
        df_for_chosen_vacancy = df[df['name'].str.contains(chosen_vacancy, case=False)]

        self.salary_average = round(df.apply(lambda x: x['salary'] / 2, axis=1).mean())
        self.salary_average_for_chosen_vacancy = round(df_for_chosen_vacancy.apply(lambda x: x['salary'] / 2, axis=1).mean())
        self.vacancy_count = df.shape[0]
        self.chosen_vacancy_count = df_for_chosen_vacancy.shape[0]

        self.year = year


class Analytic:
    """Класс анализирует и сохраняет информацию о вакансиях по годам

    Attributes:
        df (DateFrame): исходная таблица с данным
        chosen_vacancy (str): название выбранной вакансии
    """
    def __init__(self, file_name: str, chosen_vacancy: str):
        """Метод инициализирует класс Analytic

        Params:
            file_name (str): путь до файла до исходной CSV-таблицы
            chosen_vacancy (str): название выбранной вакансии
        """
        self.df = pd.read_csv(file_name)
        self.chosen_vacancy = chosen_vacancy

    def get_file_analytic(self) -> list[YearInformation]:
        """Метод возвращает список экземпляров класса YearInformation

        Returns:
            list[YearInformation]: список экземпляров класса YearInformation
        """
        self.df['year'] = self.df['published_at'].apply(lambda x: x[:4])
        groups = self.df.groupby(['year'])
        rows = [YearInformation(df, self.chosen_vacancy, year) for year, df in groups]
        return rows

    def generate_pdf(self):
        """Метод рендерит PDF отчёт из HTML шаблона и сохраняет его (отчёт)
        """
        template = Environment(loader=FileSystemLoader(TEMPLATES)).get_template(TEMPLATE)
        pdf_template = template.render({'name': self.chosen_vacancy, 'rows': self.get_file_analytic()})
        pdfkit.from_string(pdf_template, 'report_3_4_2.pdf', options={"enable-local-file-access": ""})


if __name__ == '__main__':
    analytic = Analytic(PATH_TO_INPUT_FILE, VACANCY_NAME)
    analytic.generate_pdf()