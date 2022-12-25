import grequests
import pandas as pd


COLUMNS = ['name', 'salary_from', 'salary_to', 'salary_currency', 'area_name', 'published_at']
PATH_TO_OUTPUT_FILE = '../data/api_vacancies.csv'


class Vacancies:
    """Класс получает данные по API hh.ru на 15.12 и записывает результаты в CSV-файл
    """

    @staticmethod
    def get_url(page, date_from, date_to):
        """Метод возвращает корректный URL, по которому можно сделать запрос к API hh.ru

        Params:
            page (int): номер страницы
            date_from (str): левая граница даты
            date_to (str): правая граница даты

        Returns:
            (str): URL, по которому можно сделать запрос к API hh.ru
        """
        return 'https://api.hh.ru/vacancies?specialization=1&per_page=100&page={0}&date_from={1}&date_to={2}'.format(page, date_from, date_to)

    @staticmethod
    def parse_vacancy(vacancy):
        """Метод получает форматированную информацию о вакансии

        Params:
            vacancy (dict): словарь с информацией по вакансии, которую мы получаем по API

        Returns:
            tuple: информация по вакансии
        """
        name, area_name, published_at = vacancy['name'], vacancy['area']['name'], vacancy['published_at']
        salary_from, salary_to, salary_currency = None, None, None
        salary = vacancy['salary']
        if salary:
            salary_from = salary['from']
            salary_to = salary['to']
            salary_currency = salary['currency']
        return name, salary_from, salary_to, salary_currency, area_name, published_at


    def get_vacancies(self):
        """Метод делает запросы по API на hh.ru, получает вакансии, записывает их в CSV-файл и выводит количество найденных вакансий на 15.12
        """
        urls = [*[self.get_url(page, '2022-12-15T00:00:00', '2022-12-15T08:00:00') for page in range(20)],
                *[self.get_url(page, '2022-12-15T08:00:00', '2022-12-15T16:00:00') for page in range(20)],
                *[self.get_url(page, '2022-12-15T16:00:00', '2022-12-16T00:00:00') for page in range(20)]]

        responses = (grequests.get(url) for url in urls)
        vacancies = []

        for response in grequests.map(responses):
            for vacancy in response.json()['items']:
                vacancies.append(self.parse_vacancy(vacancy))

        df = pd.DataFrame(data=vacancies, columns=COLUMNS)
        df.to_csv(PATH_TO_OUTPUT_FILE, index=False)

        print('Всего вакансий найдено на 15.12: {0}'.format(df.shape[0]))


if __name__ == '__main__':
    vacancies_instance = Vacancies()
    vacancies_instance.get_vacancies()

