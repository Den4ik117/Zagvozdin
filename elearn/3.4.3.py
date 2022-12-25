import pandas as pd
from jinja2 import Environment, FileSystemLoader
import pdfkit


PATH_TO_INPUT_FILE = '../data/converted_vacancies_dif_currencies_full.csv'
TEMPLATES = '../templates'
TEMPLATE = 'template_3_4_3.html'
VACANCY_NAME = 'Дизайнер'
AREA_NAME = 'Москва'


class Stats:
    """Класс ― подобие DTO-объекта, который хранит в себе данные об анализе CSV-файла

    Attributes:
        chosen_vacancy (str): выбранная вакансия
        area_name (str): название территории, по которой будет происходить поиск
        salaries (list): уровень зарплат по городам
        frequencies (list): доля вакансий по городам
        chosen (list): динамика зарплат и количества вакансий по выбранному региону и выбранной профессии
    """
    def __init__(self, chosen_vacancy: str, area_name: str):
        """Метод инициализирует класс Stats

        Params:
            chosen_vacancy (str): выбранная вакансия
            area_name (str): название территории, по которой будет происходить поиск
        """
        self.chosen_vacancy = chosen_vacancy
        self.area_name = area_name
        self.salaries = []
        self.frequencies = []
        self.chosen = []


class Analytic:
    """Класс анализирует данные о вакансиях и генерирует отчёт

    Attributes:
        df (DateFrame): исходная таблица с данным
        chosen_vacancy (str): название выбранной вакансии
        chosen_area_name (str): выбранная территория, по которой будет осуществляться поиск
        stats (Stats): экземпляр класса Stats
    """
    def __init__(self, file_name, vacancy_name: str, area_name: str):
        """Метод инициализирует класс Analytic

        Params:
            file_name (str): путь до исходной CSV-таблицы
            vacancy_name (str): название выбранной вакансии
            area_name (str): выбранная территория, по которой будет осуществляться поиск
        """
        self.df = pd.read_csv(file_name)
        self.chosen_vacancy = vacancy_name
        self.chosen_area_name = area_name
        self.stats = Stats(vacancy_name, area_name)

    def analyze_cities(self):
        """Метод анализирует информацию по городам
        """
        rows = self.df.shape[0]
        group = self.df.groupby(['area_name'])
        new_df = pd.DataFrame()
        new_df['freq'] = [value.shape[0] / rows for area_name, value in group]
        new_df['city'] = [area_name for area_name, value in group]
        new_df['salary'] = [value['salary'].mean() for area_name, value in group]
        new_df = new_df[new_df['freq'] >= 0.01]
        new_df1 = new_df.sort_values(by=['salary'], ascending=False)[['city', 'salary']].head(10)
        self.stats.salaries = [(a['city'], round(a['salary'])) for index, a in new_df1.iterrows()]
        new_df2 = new_df.sort_values(by=['freq'], ascending=False)[['city', 'freq']].head(10)
        self.stats.frequencies = [(a['city'], round(a['freq'], 4)) for index, a in new_df2.iterrows()]

    def analyze_chosen_vacancies(self):
        """Метод анализирует информацию по выбранной профессии в выбранном регионе
        """
        data = self.df[(self.df['area_name'] == self.chosen_area_name) & (self.df['name'].str.contains(self.chosen_vacancy, case=False))]
        data['year'] = data['published_at'].apply(lambda x: x[:4])
        groups = data.groupby(['year'])
        for year, df in groups:
            self.stats.chosen.append({
                'year': year,
                'salary': round(df['salary'].mean()),
                'count': df.shape[0]
            })

    def generate_pdf(self):
        """Метод генерирует PDF-отчёт из HTML шаблона, приготовленного заранее
        """
        template = Environment(loader=FileSystemLoader(TEMPLATES)).get_template(TEMPLATE)
        pdf_template = template.render({'stats': self.stats})
        pdfkit.from_string(pdf_template, 'report_3_4_3.pdf', options={"enable-local-file-access": ""})


if __name__ == '__main__':
    analytic = Analytic(PATH_TO_INPUT_FILE, VACANCY_NAME, AREA_NAME)
    analytic.analyze_chosen_vacancies()
    analytic.analyze_cities()
    analytic.generate_pdf()