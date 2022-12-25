import concurrent.futures

import pandas as pd
import os
import cProfile


class Analytics:
	"""Класс Analytics предоставляет методы для сбора информации из csv-файлов

	Attributes:
		__directory_name__ (str): Название директории с csv-файлами
		__vacancy_name__ (str): Название вакансии
		analyzed_data list[tuple]: Список кортежей с сырыми данными
		files (list[str]): Лист со всеми CSV-чанками
	"""
	def __init__(self, directory_name, vacancy_name):
		"""Инициализирует объект Analytics

		Params:
			directory_name (str): Название директории с csv-файлами
			vacancy_name (str): Название вакансии
		"""
		self.__directory_name__ = directory_name
		self.__vacancy_name__ = vacancy_name
		self.analyzed_data = []
		self.files = os.listdir(self.__directory_name__)

	def get_files_analytics(self):
		"""Анализирует все файлы из директории и сохраняет в поле analyzed_data"""

		with concurrent.futures.ProcessPoolExecutor() as executor:
			self.analyzed_data = [result for result in executor.map(self.get_chunk_analytic, self.files)]

	def get_chunk_analytic(self, file_name):
		"""Возвращает параметры аналитики одного файла

		Attributes:
			file_name (str): Название csv-файла

		Returns:
			year (int): Год публикации вакансии
			average_salary (int): Средняя зарплата по всем вакансиям
			this_vacancy_salary_average (int): Cредняя зарплата по выбранной вакансии
			count (int): Количество вакансий
			this_vacancy_count (int): Количество предложений по выбранной вакансии
		"""
		data = pd.read_csv('{0}/{1}'.format(self.__directory_name__, file_name))
		data['average'] = data[['salary_from', 'salary_to']].mean(axis=1)
		vacancy_data = data[data['name'].str.contains(self.__vacancy_name__, case=False)]
		average_salary = round(data['average'].mean())
		this_vacancy_salary_average = round(vacancy_data['average'].mean())
		count = data.shape[0]
		this_vacancy_count = vacancy_data.shape[0]
		year = int(data['published_at'][0][:4])
		return year, average_salary, this_vacancy_salary_average, count, this_vacancy_count

	def get_converted_data(self):
		"""Берет сырые данные из поля analyzed_data и разбивает их на словари
		В словаре ключ - год, значение параметр аналитики (средняя зарплата, количество вакансий и т.д.)

		Returns:
			salary (dict): Средняя зарплата по годам
			vacancies_amount (dict): Количество вакансий по годам
			this_vacancy_salary (dict): Средняя зарплата для выбранной вакансии по годам
			vacancy_amount (dict): Количество вакансий для выбранной вакансии по годам
		"""
		salary, vacancies_amount, this_vacancy_salary, vacancy_amount = {}, {}, {}, {}
		for year, avg_salary, this_avg_salary, amount, this_vacancy_amount in self.analyzed_data:
			salary[year] = avg_salary
			vacancies_amount[year] = amount
			this_vacancy_salary[year] = this_avg_salary
			vacancy_amount[year] = this_vacancy_amount
		return salary, vacancies_amount, this_vacancy_salary, vacancy_amount

	def print_data(self):
		"""Берет конвертированные данные из метода get_converted_data и печатает их
		"""
		salary, vacancies_amount, this_vacancy_salary, this_vacancy_amount = self.get_converted_data()
		print('Динамика уровня зарплат по годам: {0}'.format(salary))
		print('Динамика количества вакансий по годам: {0}'.format(vacancies_amount))
		print('Динамика уровня зарплат по годам для выбранной профессии: {0}'.format(this_vacancy_salary))
		print('Динамика количества вакансий по годам для выбранной профессии: {0}'.format(this_vacancy_amount))


if __name__ == '__main__':
	profile = cProfile.Profile()
	profile.enable()
	analytics = Analytics('../chunks', 'Аналитик')
	analytics.get_files_analytics()
	# analytics.print_data()
	profile.disable()
	profile.print_stats(1)