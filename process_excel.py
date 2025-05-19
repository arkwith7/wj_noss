import openpyxl
from competency_unit import cu_excel, lesson_plan_practical, lesson_plan_theory

def get_first_excel():
    import os
    for file in os.listdir('./input'):
        if file.lower().endswith('.xlsx'):
            return "./input/" + file
    return None

def read_excel_pages(excel_file):
    workbook = openpyxl.load_workbook(excel_file, read_only=True)
    excel_data = {}

    for sheet_name in workbook.sheetnames:
        print(sheet_name)
        sheet = workbook[sheet_name]
        excel_data[sheet_name] = sheet  # Store the sheet object directly

    return excel_data

def process_excel(excel_file) -> cu_excel:
    if not excel_file:
        print("No Excel file found in the input directory.")
        raise Exception("No excel file found")
    
    excel_pages = read_excel_pages(excel_file)

    cu_excel_data = cu_excel()

    for row in excel_pages["JPMPBP"]:
        if len(row) >= 5:  # Ensure there are enough elements in the row
            lpp = lesson_plan_practical()
            lpp.work_activities = row[1].value
            lpp.lp_title = row[2].value
            lpp.duration = row[3].value
            lpp.learning_objectives = row[4].value
            cu_excel_data.lpps.append(lpp)

    for row in excel_pages["JPMPBT"]:
        if len(row) >= 5:  # Ensure there are enough elements in the row
            lpt = lesson_plan_theory()
            lpt.work_activities = row[1].value
            lpt.lp_title = row[2].value
            lpt.duration = row[3].value
            lpt.learning_objectives = row[4].value
            cu_excel_data.lpts.append(lpt)
    
    return cu_excel_data
