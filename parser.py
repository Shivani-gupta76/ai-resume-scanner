# parser.py
from pdfminer.high_level import extract_text
import docx

def extract_text_from_pdf(file_path):
    return extract_text(file_path)

def extract_text_from_docx(file):
    doc = docx.Document(file)
    return "\n".join([para.text for para in doc.paragraphs])

def extract_resume_text(file, filename):
    if filename.endswith(".pdf"):
        return extract_text_from_pdf(file)
    elif filename.endswith(".docx"):
        return extract_text_from_docx(file)
    else:
        return ""
