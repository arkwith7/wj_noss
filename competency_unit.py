
class lesson_plan_practical:
    work_activities = ""
    lp_title = ""
    duration = 0
    learning_objectives = []

class lesson_plan_theory:
    work_activities = ""
    lp_title = ""
    duration = 0
    learning_objectives = []

class cu_excel:
    lpps: list[lesson_plan_practical] = []
    lpts: list[lesson_plan_theory] = []
    
class competency_unit:

    def __init__(self, parsed_pdf_data):
        self.program_code = parsed_pdf_data.get('Program code', '')
        self.program_name = parsed_pdf_data.get('Program name', '')
        self.program_level = parsed_pdf_data.get('Level', '')
        self.competency_unit_name = parsed_pdf_data.get('Competency unit', '')
        self.competency_unit_title = parsed_pdf_data.get('Competency unit title', '')
        self.no_and_statement_of_work_activities = parsed_pdf_data.get('Work activities list', '')

    program_code = ""
    program_name = ""
    program_level = ""
    competency_unit_name = ""
    competency_unit_title = ""
    no_and_statement_of_work_activities = []
    
    references = []

    cu_excel_data: cu_excel = cu_excel()
