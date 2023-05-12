import os

from PIL import Image
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_text():

    text_extracted = pytesseract.image_to_string(Image.open('./static/Images/equation.png'))

    folder_path = './static/Images/'

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)

    return text_extracted
