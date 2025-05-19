import os
from docx import Document
from datetime import datetime

from competency_unit import lesson_plan_theory, lesson_plan_practical

def get_first_docx_template():
    template_dir = 'templates'
    for file in os.listdir(template_dir):
        if file.lower().endswith('.docx'):
            return os.path.join(template_dir, file)
    return None