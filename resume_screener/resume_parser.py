import textract

def extract_text_from_pdf(pdf_path):
    try:
        text = textract.process(pdf_path).decode('utf-8')
        return text
    except Exception as e:
        return f"Error reading {pdf_path}: {str(e)}"
