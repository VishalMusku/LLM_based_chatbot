import pdfplumber

def extract_text_save_to_file(pdf_path, output_file_path):
    with pdfplumber.open(pdf_path) as pdf:
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            for page_number, page in enumerate(pdf.pages):
                output_file.write(f"--- Page {page_number + 1} ---\n")
                text = page.extract_text()
                if text:
                    normalized_text = '\n'.join(line.strip() for line in text.split('\n') if line.strip())
                    output_file.write(normalized_text + "\n\n")
                # tables = page.extract_tables()
                # for table in tables:
                #     output_file.write("[Table Start]\n")
                #     for row in table:
                #         row = ['' if cell is None else str(cell).strip() for cell in row]
                #         output_file.write('\t'.join(row) + '\n')
                #     output_file.write("[Table End]\n\n")
