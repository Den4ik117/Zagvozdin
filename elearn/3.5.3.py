import sqlite3
import pandas as pd


DATABASE = '../database/database.db'
VACANCY = 'Аналитик'


if __name__ == '__main__':
    conn = sqlite3.connect(DATABASE)

    total_vacancies = conn.execute("SELECT COUNT(*) FROM `vacancies`").fetchone()[0]

    df1 = pd.read_sql("SELECT ROUND(AVG(salary)) as average, strftime('%Y', published_at) as year FROM `vacancies` GROUP BY year", conn)
    df2 = pd.read_sql("SELECT COUNT(*) as count_of_vacancies, strftime('%Y', published_at) as year FROM `vacancies` GROUP BY year", conn)
    df3 = pd.read_sql("SELECT ROUND(AVG(salary)) as average, strftime('%Y', published_at) as year FROM `vacancies` WHERE `name` LIKE \"%{0}%\" GROUP BY year".format(VACANCY), conn)
    df4 = pd.read_sql("SELECT COUNT(*) as count_of_vacancies, strftime('%Y', published_at) as year FROM `vacancies` WHERE `name` LIKE \"%{0}%\" GROUP BY year".format(VACANCY), conn)
    df5 = pd.read_sql("SELECT ROUND(AVG(salary)) as average, area_name, COUNT(*) as count_of_vacancies FROM `vacancies` GROUP BY area_name HAVING count_of_vacancies > {0} ORDER BY average DESC LIMIT 10".format(round(total_vacancies * 0.01)), conn)
    df6 = pd.read_sql("SELECT area_name, COUNT(*) / {0}.0 as frequency FROM `vacancies` GROUP BY area_name ORDER BY frequency DESC LIMIT 10".format(total_vacancies), conn)

    print(df1)
    print(df2)
    print(df3)
    print(df4)
    print(df5)
    print(df6)
