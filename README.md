## Репозиторий с заданиями с ELearn

### Тестирование

Сделал тестирование на doctest и модульных тестах.

5 методов протестировано в файле `main.py`.
3 метода протестировано _доктестами_, 2 метода ― _модульными тестами_.
Все пограничные случаи учтены.

#### doctests
![doctests](images/image_1.png)

#### Модульные тесты
![Модульные тесты](images/image_2.png)

### Профилирование

Сделал профилирование 6 методов для обработки сырой даты в формат `dd.mm.YYYY`.
По итогам профилирования самым эффективным и быстрым методом оказался `fourth_date_parser()`.
Остальные методы закомментировал, оставил только самый эффективный.
Результаты профилирования прикрепляю ниже.

#### first_date_parser()
![first_date_parser](images/image_3.png)

#### second_date_parser()
![second_date_parser](images/image_4.png)

#### third_date_parser()
![third_date_parser](images/image_5.png)

#### fourth_date_parser()
![fourth_date_parser](images/image_6.png)

#### fifth_date_parser()
![fifth_date_parser](images/image_7.png)

#### sixth_date_parser()
![sixth_date_parser](images/image_8.png)


### Разделение одного большого CSV-файла на чанки
![chunks](images/image_9.png)

### Многопроцессорная обработка

#### Без многопроцессорной обработки
![without_multiprocessing](images/image_10.png)

#### Multiprocessing
![with_multiprocessing](images/image_11.png)

#### concurrent.futures
![concurrent.futures](images/image_12.png)

### Курсы валют

#### Частотность, с которой встречаются различные валюты
![Частотность, с которой встречаются различные валюты](images/image_13.png)

#### Полученный DataFrame в CSV формате 
![Полученный DataFrame в CSV формате](images/image_14.png)

### Конвертация валют

#### Первые 100 результатов в формате CSV

![Конвертация валют](images/image_15.png)

### Курсы валют в БД

![Курсы валют в БД](images/image_16.png)

### Вакансии в БД

Примечание. Для экономии места и ресурсов операции делал только для первых 100 записей.

![Вакансии в БД](images/image_17.png)