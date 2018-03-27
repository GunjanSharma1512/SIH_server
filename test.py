import hashlib
import hashlib
import io
import PIL
from PIL import Image
##with open("image.png", "rb") as imageFile:
  #  f = imageFile.read()
   # b = bytearray(f)
#print(b.encode('base64'))
"""
filein = "image.jpeg"
img = Image.open(filein)
fileout = "image1.bmp"
img.save(fileout)

hash = hashlib.md5()
hash.update(open('image.jpeg', 'rb').read())
print((hash.digest()).encode('base64'))

img = Image.open('image.jpeg')
m = hashlib.md5()
with io.BytesIO() as memf:
    img.save(memf, 'JPEG')
    data = memf.getvalue()
    m.update(data)
    
print(m.hexdigest())
"""
print("jQYom/6MsRM0nZmR7LONCA==".decode('base64'))