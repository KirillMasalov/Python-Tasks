from DataSet_class import DataSet
from Report_class import Report


file_name = input("Введите название файла: ")
current_vacancy_name = input("Введите название профессии: ")

data = DataSet(current_vacancy_name)
data.fill_dictionaries(DataSet.csv_reader(file_name), current_vacancy_name)
data.calculate_vacancies_count()
data.fill_statistics_dictionaries()

sorted_salaries_by_town = dict(sorted(data.salaries_by_town.items(), key=lambda item: item[1], reverse=True)[0:10])
sorted_vacancies_by_rate = dict(sorted(data.vacancies_rate_by_town.items(),
                                       key=lambda item: item[1], reverse=True)[0:10])

report = Report()
report.generate_image(data, sorted_salaries_by_town, sorted_vacancies_by_rate, current_vacancy_name)
