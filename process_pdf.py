import PyPDF2

def get_first_pdf():
    import os
    for file in os.listdir('./input'):
        if file.lower().endswith('.pdf'):
            return "./input/" + file
    return None

def find_topic_and_subcategories(toc, topic, pdf_reader):
    results = []
    subcategories = []
    
    def search_toc(entries, depth=0, parent=None):
        for entry in entries:
            if isinstance(entry, list):
                search_toc(entry, depth + 1, parent)
            else:
                if parent and topic.lower() in parent['/Title'].lower():
                    page_num = pdf_reader.get_destination_page_number(entry)
                    subcategories.append((entry['/Title'], page_num))
                elif topic.lower() in entry['/Title'].lower():
                    page_num = pdf_reader.get_destination_page_number(entry)
                    results.append((entry['/Title'], page_num))
                    if isinstance(entries, list) and entries.index(entry) + 1 < len(entries):
                        next_entry = entries[entries.index(entry) + 1]
                        if isinstance(next_entry, list):
                            search_toc(next_entry, depth + 1, entry)
    
    search_toc(toc)
    return results, subcategories

def get_page_number(pdf_reader, entry):
    if isinstance(entry, list):
        return get_page_number(pdf_reader, entry[0])
    return pdf_reader.get_destination_page_number(entry)

# Process the PDF and return the competency units as sets of pages
def process_pdf(pdf_file):
    with open(pdf_file, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        pdf_pages = [page.extract_text() or "[Unable to extract text from this page]" for page in pdf_reader.pages]
        toc = pdf_reader.outline
    
    curriculum_results, subcategories = find_topic_and_subcategories(toc, "Curriculum of Competency Unit", pdf_reader)
    
    if curriculum_results:
        main_topic = curriculum_results[0]
        print(f"\nFound '{main_topic[0]}' on page {main_topic[1]}")
        
        if subcategories:
            print("\nSubcategories:")
            for title, page in subcategories:
                print(f"- {title} (Page: {page})")
            
            chunks = []
            for i, (title, start_page) in enumerate(subcategories):
                if i + 1 < len(subcategories):
                    end_page = subcategories[i+1][1] - 1
                else:
                    next_main_section = next((entry for entry in toc if get_page_number(pdf_reader, entry) > start_page), None)
                    end_page = get_page_number(pdf_reader, next_main_section) - 1 if next_main_section else len(pdf_pages)
                
                chunk = "\n".join(pdf_pages[start_page-1:end_page])
                chunks.append((title, start_page, end_page, chunk))
            
            return chunks
        else:
            print("\nNo subcategories found for 'Curriculum of Competency Unit'.")
    else:
        print("\n'Curriculum of Competency Unit' not found in the table of contents.")
    
    return []
