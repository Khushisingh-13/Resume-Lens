import fitz
def extract_text_from_pdf(file):
    pdf = fitz.open(
        stream=file.read(),
        filetype="pdf"
    )
    text = ""
    for page in pdf:
        text += page.get_text()

    pdf.close()
    return text