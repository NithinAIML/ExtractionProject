import pytesseract
from  PyPDF2 import PdfReader
from PIL import Image
import re

""" Method extract_text_from_pdf works on the basis of pyPDF2, which reads pdf and performs text extraction on it, Once the text is extracted
    from the image, I have performed an operation where I iterate on each rows based on the lookup terms on each row, once I get retrieved
    rows then performed parition to based on the lookup terms and selected the desired output """

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


""" Method extract_text_from_image works on pytesseract ocr, which will extract text from images, here I have used regex pattern and iterated text
    on text of each row by using findall method and then considering the very first from all the rows which matched the pattern and giving
    as a desired output """


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

""" Look up terms for PDF and calling extract_text_from_pdf function """

look_up_terms = ['positive', 'negative']
pdf_text = extract_text_from_pdf("Data\\Breast-IHC-report-sample.pdf", look_up_terms=look_up_terms)
print("Output from PDF:")
print(pdf_text)

""" Calling extract_text_from_img function """

jpg_text = extract_text_from_img("Data\\biomarker_result.jpg")
print("\nOutput from Image:")
print(jpg_text)