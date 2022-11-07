from DataSet_class import DataSet
from openpyxl import Workbook
from openpyxl.styles import Font, Border, Side
from openpyxl.styles.numbers import FORMAT_PERCENTAGE_00

border = Border(left=Side(border_style='thin', color='FF000000'),
                right=Side(border_style='thin', color='FF000000'),
                top=Side(border_style='thin', color='FF000000'),
                bottom=Side(border_style='thin', color='FF000000'),)

font = Font(bold=True)


class Report:
    def __init__(self, border: Border = border, font: Font = font):
        self.__border = border
        self.__headline_font = font

    def generate_excel(self, data: DataSet, salaries_by_town: dict, rates_by_town: dict, current_vacancy_name: str):
        wb = Workbook()
        years_sheet = wb.active
        self.__fill_year_sheet(years_sheet, data, current_vacancy_name)

        town_sheet = wb.create_sheet("Статистика по городам")
        self.__fill_town_sheet(town_sheet, salaries_by_town, rates_by_town)

        for column in ["A", "B", "C", "D", "E"]:
            years_sheet.column_dimensions[column].width =\
                max(list(map(lambda cell: len(str(cell.value)), years_sheet[column]))) + 2
            town_sheet.column_dimensions[column].width = \
                max(list(map(lambda cell: len(str(cell.value)), town_sheet[column]))) + 2

        wb.save("report.xlsx")

    def __fill_year_sheet(self, sheet, data, current_vacancy_name):
        sheet.title = "Статистика по годам"
        sheet.append(["Год", "Средняя зарплата", "Средняя зарплата - " + current_vacancy_name,
                      "Количество вакансий", "Количество вакансий - " + current_vacancy_name])

        for year in data.salaries_by_year.keys():
            sheet.append([year, data.salaries_by_year[year], data.current_salaries_by_year[year],
                          data.vacancies_count_by_year[year], data.current_count_by_year[year]])

        for row in sheet:
            for cell in row:
                if cell.row == 1:
                    cell.font = self.__headline_font
                cell.border = self.__border

    def __fill_town_sheet(self, sheet, salaries_by_town, rates_by_town):
        sheet.append(["Город", "Уровень зарплат", " ", "Город", "Доля вакансий"])

        town_rows = []
        for town_item in salaries_by_town.items():
            town_rows.append([town_item[0], town_item[1], " "])

        for i, town_item in enumerate(rates_by_town.items()):
            town_rows[i] += [town_item[0], town_item[1]]
            sheet.append(town_rows[i])

        for row in sheet:
            for cell in row:
                if cell.column == 3:
                    continue
                if cell.row == 1:
                    cell.font = self.__headline_font
                cell.border = self.__border
                if cell.column == 5:
                    cell.number_format = FORMAT_PERCENTAGE_00