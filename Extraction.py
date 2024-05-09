import pytesseract
from  PyPDF2 import PdfReader
from PIL import Image
import re



def extract_text_from_pdf(pdf_path, look_up_terms):
    text = ""
    content = ""
    with open(pdf_path, 'rb') as file:
        pdf_reader = PdfReader(file)
        for page in pdf_reader.pages:
            text += page.extract_text()
            rows = text.split('\n')
            for row in rows:
                for i in look_up_terms:
                    if i in row.lower() and not len(row.split()) > 6:
                        part_value = row.lower().partition(i)
                        content += part_value[0].capitalize() + i.capitalize() + ' IHC\n'
                        break
    return content


def extract_text_from_img(img_path):
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'
    text = pytesseract.image_to_string(Image.open(img_path))
    rows = text.split('\n')
    pattern = "^[A-Z\d]+ [A-Z\d]+"
    result = ""
    for row in rows:
        matches = re.findall(pattern, row)
        if matches:
            out = ", ".join(matches[0].split())
            if result:
                result += " N/A \n " + out
            else:
                result += out
    return result

look_up_terms = ['positive', 'negative']
pdf_text = extract_text_from_pdf("Data\\Breast-IHC-report-sample.pdf", look_up_terms=look_up_terms)
print("Output from PDF:")
print(pdf_text)

jpg_text = extract_text_from_img("Data\\biomarker_result.jpg")
print("\nOutput from Image:")
print(jpg_text)