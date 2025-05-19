import google.generativeai as genai
from process_pdf import get_first_pdf, process_pdf
from process_excel import process_excel
from competency_unit import competency_unit
import json
import os

# TODO: Fill in the Google API key
GOOGLE_API_KEY = ""

# Configure the API key
genai.configure(api_key=GOOGLE_API_KEY)

# Initialize the model
# This can be changed to gemini-1.5-pro for more powerful results
model = genai.GenerativeModel('gemini-1.5-flash')

# Get user inputs
# This is probably going to have to be per CU, so we move it into the CU loop below
#document_number = int(input("Enter the document number: "))
#total_documents = int(input("Enter the total number of documents: "))

competency_units: list[competency_unit] = []

# Find the first PDF file
# TODO: Make this an argument

pdf_file = get_first_pdf()
cu_pdf_data_parsed = None
if pdf_file:
    competency_units_pdf_data = process_pdf(pdf_file)
    
    for title, start_page, end_page, chunk in competency_units_pdf_data:
        prompt = f"""
        You are an expert at extracting fields from PDF documents.

        Analyze the following PDF data and extract the following fields, and output the fields in a json format. Do not nest data. Do not include fields not listed in <Fields>, and do not include any other text outside of the json. When fields appear corrupted by the pdf format, like spaces or newlines in unexpected places, repair the data.
        <Fields>
            Program code
            Program name
            Level
            Competency unit
            Competency unit title
            Work activities list
        </Fields>

        Content:
        {chunk}
        """

        # Generate content based on the PDF chunk
        response = model.generate_content(prompt)
        
        # Print the response for each chunk
        print(f"\nResponse for '{title}' (Pages {start_page} - {end_page}):")
        print(response.text)
        print("\n" + "="*50 + "\n")

        # Parse the JSON response
        try:
            cu_pdf_data_parsed = json.loads(response.text.replace("```", "").replace("json", ""))
        except json.JSONDecodeError as e:
            print(f"Error: Unable to parse JSON response: {e}")

        cu = competency_unit(cu_pdf_data_parsed)
        competency_units.append(cu)
else:
    print("No PDF file found in the current directory.")

# Read Excel and associate with PDF CUs
# Read all Excel files in input/cu_excel_sheets
excel_files = []
excel_dir = 'input/cu_excel_sheets'

for file in os.listdir(excel_dir):
    if file.lower().endswith('.xlsx'):
        excel_files.append(os.path.join(excel_dir, file))

if not excel_files:
    print("No Excel files found in the input/cu_excel_sheets directory.")
    raise Exception("No Excel files found")

for file in excel_files:
    excel_data = process_excel(file)
    # Find matching competency unit for the Excel data
    matching_cu = None
    for cu in competency_units:
        if cu.competency_unit_name == excel_data.lpps[0].work_activities or cu.competency_unit_name == excel_data.lpts[0].work_activities:
            matching_cu = cu
            break
    
    if matching_cu:
        matching_cu.cu_excel_data = excel_data
        print(f"Matched Excel data to Competency Unit: {matching_cu.competency_unit_name}")
    else:
        print("No matching Competency Unit found for the Excel data")

# Populate each template for each lesson plan

for cu in competency_units:

    # LPP
    lpp_templates = []
    lpp_template_dir = 'templates/lpp'

    for file in os.listdir(lpp_template_dir):
        if file.lower().endswith('.docx'):
            lpp_templates.append(os.path.join(lpp_template_dir, file))

    # LPT
    lpt_templates = []
    lpt_template_dir = 'templates/lpt'

    for file in os.listdir(lpt_template_dir):
        if file.lower().endswith('.docx'):
            lpt_templates.append(os.path.join(lpt_template_dir, file))
