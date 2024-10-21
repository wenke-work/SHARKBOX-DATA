import pytesseract
from PIL import Image


pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
img = Image.open('C:\\Users\\Administrator\\Desktop\\files\\temp\\tmp\\1.png')
text = pytesseract.image_to_string(img,lang='chi_sim')
print(text)