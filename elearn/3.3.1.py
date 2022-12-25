import pandas as pd
import xmltodict
import grequests


PATH_TO_INPUT_FILE = '../data/vacancies_dif_currencies.csv'
PATH_TO_OUTPUT_FILE = '../data/currency_value.csv'
COLS = ['salary_from', 'salary_to', 'salary_currency', 'area_name', 'published_at']


class Worker:
	"""Класс позволяет забрать информацию о валюте за каждый месяц, используя API ЦБ

	Здесь мы используем 2 нестандартных библиотеки:
	1. xmltodict - позволяет легко конвертировать XML формат в Python-словари
	2. grequests - более быстрый и эффективный аналог стандартного модуля Python requests

	Attributes:
		data (DataFrame): информация о вакансиях
	"""
	def __init__(self, data):
		"""Метод инициализирует класс Worker

		Params:
			data (DataFrame): информация о вакансиях
		"""
		self.data = data

	@property
	def urls(self):
		"""Лист URL, к которым нужно сделать запрос

		Returns:
			list: лист URL-ов, по которым нужно обратиться по API
		"""
		return ['https://www.cbr.ru/scripts/XML_daily.asp?date_req={0[2]}/{0[1]}/{0[0]}'.format(date.split('-')) for date in self.get_range_dates()]

	@property
	def currencies_amount_items(self):
		"""Список валют и количество, сколько раз они встретились

		Returns:
			list[(string, int)]: возвращает список валют и количество, сколько раз они встретились
		"""
		return self.data['salary_currency'].value_counts().to_dict().items()

	def print_currencies_frequencies(self):
		"""Выводит в консоль информацию частотности, с которой встречаются различные валюты
		"""
		vacancies_amount = self.data.shape[0]
		result = {currency: amount / vacancies_amount for currency, amount in self.currencies_amount_items}
		print('Частотность, с которой встречаются различные валюты:\n')
		for currency, frequency in result.items():
			print('{0}: {1}'.format(currency, frequency))

	def get_range_dates(self):
		"""Метод возвращает лист всех дат за каждый месяц за определённый период

		Returns:
			 list: лист дат за каждый месяц за определённый период
		"""
		years_series = pd.to_datetime(self.data['published_at'].apply(lambda x: x[:10]))
		return pd.date_range(start=str(years_series.min())[:10], end=str(years_series.max())[:10], freq='M').strftime('%Y-%m-%d').tolist()

	def get_result_file(self):
		"""Метод создаёт словарь, который представляет собой формат DataFrame, содержащий информацию
		о валютах за определённый период каждого месяца, затем записывает этот словарь в файл
		"""
		currencies_code = list(map(lambda x: x[0], filter(lambda x: x[-1] > 5000 and x[0] != 'RUR', self.currencies_amount_items)))
		dct = {key: [] for key in ['date'] + currencies_code}
		response = (grequests.get(url) for url in self.urls)
		for r in grequests.map(response):
			data = xmltodict.parse(r.text)['ValCurs']
			dct['date'] = dct['date'] + ['{0[2]}-{0[1]}'.format(str(data['@Date']).split('.'))]
			currency_value = {code: None for code in currencies_code}
			for currency in data['Valute']:
				code = currency['CharCode']
				if code in currencies_code:
					nominal = float(currency['Nominal'])
					currency_value[code] = round(float(currency['Value'].replace(',', '.')) / nominal, 6)
			for code, value in currency_value.items():
				dct[code] = dct[code] + [value]
		pd.DataFrame(dct).to_csv(path_or_buf=PATH_TO_OUTPUT_FILE, index=False, encoding='utf-8-sig')


if __name__ == '__main__':
	df = pd.read_csv(PATH_TO_INPUT_FILE, usecols=COLS)
	filtered_data = df[pd.notnull(df['salary_currency']) & df['salary_currency'].notna()]
	worker = Worker(filtered_data)
	worker.get_result_file()
	# worker.print_currencies_frequencies()
