'''==========================================
; Title:  OCR using Pytesser lib
; Author: Akshama
; Date:   22 Oct 2017
;==========================================
Reference: http://www.manejandodatos.es/2014/11/ocr-python-easy/
'''

from PIL import Image
from pytesseract import *
pytesseract.pytesseract.tesseract_cmd = 'C:\Users\Gunjan'

#Your image file's name goes here

text = image_to_string(Image.open("image_test5.jpeg",'r'))
print text