from Vacancy_class import Vacancy
import csv


class DataSet:
    def __init__(self, profession_name: str):
        self.__vacancies_count_by_year = {}
        self.__sum_salaries_by_year = {}
        self.__current_count_by_year = {}
        self.__current_sum_salary_by_year = {}
        self.__vacancies_count_by_town = {}
        self.__sum_salaries_by_town = {}
        self.__vacancies_count = 0
        self.__current = profession_name

        self.__salaries_by_year = {}
        self.__current_salaries_by_year = {}
        self.__salaries_by_town = {}
        self.__vacancies_rate_by_town = {}

    @property
    def vacancies_count(self):
        return self.__vacancies_count

    @property
    def salaries_by_year(self):
        return self.__salaries_by_year

    @property
    def vacancies_count_by_year(self):
        return self.__vacancies_count_by_year

    @property
    def current_salaries_by_year(self):
        return self.__current_salaries_by_year

    @property
    def current_count_by_year(self):
        return self.__current_count_by_year

    @property
    def salaries_by_town(self):
        return self.__salaries_by_town

    @property
    def vacancies_rate_by_town(self):
        return self.__vacancies_rate_by_town

    @staticmethod
    def csv_reader(file_name: str) -> []:
        data = []
        with open(file_name, "r", encoding="UTF-8-sig") as file:
            file_reader = csv.DictReader(file, delimiter=",")
            headlines_list = list(file_reader.fieldnames)
            for line in file_reader:
                vacancy = DataSet.parse_line_to_vacancy(line, headlines_list)
                if vacancy is not None:
                    data.append(vacancy)
        return data

    @staticmethod
    def parse_line_to_vacancy(line, headlines_list):
        vacancy_dict = {}
        for headline in headlines_list:
            vacancy_dict[headline] = line[headline]
        if "" not in vacancy_dict.values():
            return Vacancy(vacancy_dict)
        return None

    def fill_dictionaries(self, data: [Vacancy], current_vacancy_name):
        for vacancy in data:
            key = int(vacancy.year)
            self.__vacancies_count_by_year[key] = self.__vacancies_count_by_year.setdefault(key, 0) + 1
            self.__sum_salaries_by_year[key] = self.__sum_salaries_by_year.setdefault(key, 0) \
                                               + vacancy.average_ru_salary
            self.__vacancies_count_by_town[vacancy.area_name] = \
                self.__vacancies_count_by_town.setdefault(vacancy.area_name, 0) + 1
            self.__sum_salaries_by_town[vacancy.area_name] = \
                self.__sum_salaries_by_town.setdefault(vacancy.area_name, 0) + vacancy.average_ru_salary

            if current_vacancy_name in vacancy.name:
                self.__current_count_by_year[key] = self.__current_count_by_year.setdefault(key, 0) + 1
                self.__current_sum_salary_by_year[key] = \
                    self.__current_sum_salary_by_year.setdefault(key, 0) + vacancy.average_ru_salary

    def calculate_vacancies_count(self):
        self.__vacancies_count = sum(self.__vacancies_count_by_town.values())

    def fill_statistics_dictionaries(self):
        for key in self.__sum_salaries_by_year.keys():
            self.__salaries_by_year[key] = int(self.__sum_salaries_by_year[key] / (self.__vacancies_count_by_year[key]))
            if key in self.__current_count_by_year:
                self.__current_salaries_by_year[key] = int(self.__current_sum_salary_by_year[key]
                                                           / self.__current_count_by_year[key])
            else:
                self.__current_salaries_by_year[key] = 0
                self.__current_count_by_year[key] = 0

        for key in self.__sum_salaries_by_town.keys():
            if int(self.__vacancies_count_by_town[key] / self.__vacancies_count * 100) >= 1:
                self.__salaries_by_town[key] = int(self.__sum_salaries_by_town[key] /
                                                   self.__vacancies_count_by_town[key])

        for key in self.__salaries_by_town:
            self.__vacancies_rate_by_town[key] = round(self.__vacancies_count_by_town[key] / self.__vacancies_count, 4)