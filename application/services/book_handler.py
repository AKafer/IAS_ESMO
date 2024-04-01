from datetime import datetime

from openpyxl import Workbook
from openpyxl.styles import Font, Alignment


def add_null_for_hour(date: datetime) -> str:
    if date:
        date = date.strftime('%Y-%m-%d %H:%M:%S')
        date_str, time_str = date.split(' ')
        if len(time_str) < 8:
            date = date_str + ' ' + '0' + time_str
    return date


async def get_book(exams: list[dict]) -> Workbook:
    wb = Workbook()
    sheet = wb.active

    c1 = sheet.cell(row=1, column=1)
    c1.value = "№/№"
    c1.font = Font(bold=True)
    c1.alignment = Alignment(horizontal="center")
    sheet.column_dimensions['A'].width = 10

    c2 = sheet.cell(row=1, column=2)
    c2.value = "Номер работника"
    c2.font = Font(bold=True)
    c2.alignment = Alignment(horizontal="center")
    sheet.column_dimensions['B'].width = 20

    c3 = sheet.cell(row=1, column=3)
    c3.value = "Полное имя"
    c3.font = Font(bold=True)
    c3.alignment = Alignment(horizontal="center")
    sheet.column_dimensions['C'].width = 35

    c4 = sheet.cell(row=1, column=4)
    c4.value = "Тест - тип 1"
    c4.font = Font(bold=True)
    c4.alignment = Alignment(horizontal="center")
    sheet.column_dimensions['D'].width = 15

    c5 = sheet.cell(row=1, column=5)
    c5.value = "Дата"
    c5.font = Font(bold=True)
    c5.alignment = Alignment(horizontal="center")
    sheet.column_dimensions['E'].width = 20

    c6 = sheet.cell(row=1, column=6)
    c6.value = "Тест - тип 2"
    c6.font = Font(bold=True)
    c6.alignment = Alignment(horizontal="center")
    sheet.column_dimensions['F'].width = 15

    c7 = sheet.cell(row=1, column=7)
    c7.value = "Дата"
    c7.font = Font(bold=True)
    c7.alignment = Alignment(horizontal="center")
    sheet.column_dimensions['G'].width = 20

    c8 = sheet.cell(row=1, column=8)
    c8.value = "Продолжительность"
    c8.font = Font(bold=True)
    c8.alignment = Alignment(horizontal="center")
    sheet.column_dimensions['H'].width = 25

    for idx, item in enumerate(exams):
        sheet.append([
            idx + 1,
            item['number'],
            item['name'],
            item['type_1'],
            add_null_for_hour(item['date_type_1']),
            item['type_2'],
            add_null_for_hour(item['date_type_2']),
            item['duration'],
        ])
        for i in range(1, 9):
            cell = sheet.cell(row=idx + 2, column=i)
            if i in (4, 6):
                cell.alignment = Alignment(horizontal="center")
            else:
                cell.alignment = Alignment(horizontal="right")
    return wb