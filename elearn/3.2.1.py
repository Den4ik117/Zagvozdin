import pandas as pd


class Parser:
	def __init__(self, file_name):
		self.df = pd.read_csv(file_name)

	@property
	def years(self):
		return self.df['published_at'].apply(lambda x: x[:4]).unique()

	def write_chunks_to_csv(self):
		for year in self.years:
			filtered_data = self.df[self.df['published_at'].str.contains(year)]
			file_name = '../chunks/vacancies_by_{0}.csv'.format(year)
			filtered_data.to_csv(path_or_buf=file_name, index=False, encoding='utf-8-sig')


if __name__ == '__main__':
	parser = Parser('../data/vacancies_by_year.csv')
	parser.write_chunks_to_csv()