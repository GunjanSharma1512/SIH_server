'''==========================================
; Title:  OCR using Pytesser lib
; Author: Akshama
; Date:   22 Oct 2017
;==========================================
Reference: http://www.manejandodatos.es/2014/11/ocr-python-easy/
'''

from PIL import Image
from pytesseract import *
from difflib import SequenceMatcher
#Your image file's name goes here
image_file1 = 'IMG_TEST6.jpg'
image_file2 = 'IMG_TEST6_TAMPERED.jpg'
im1 = Image.open(image_file1)
im2 = Image.open(image_file2)
f1 = open("text1.txt","w")
f2 = open("text2.txt","w")
f1.write(image_to_string(im1).encode('UTF=8'))
f1.close()
f2.write(image_to_string(im2).encode('UTF=8'))
f2.close()
text1 = open("text1.txt").read()
text2 = open("text2.txt").read()
m = SequenceMatcher(None, text1, text2)
print (m.ratio())