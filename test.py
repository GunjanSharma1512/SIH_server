# -*- coding: utf-8 -*-
from __future__ import unicode_literals


import numpy as np
import cv2

from PIL import Image
from pytesseract import *
from difflib import SequenceMatcher

new_name="image_47.jpeg"
img2=Image.open(new_name)

def ocr_process(image_file1):
    #image_file1 = 'IMG_TEST6.jpg'
    image_file2 = 'img_test_f.jpg'
    img2 = Image.open(image_file2)

    im1 = Image.open(image_file1,"rb")
    im2 = Image.open(image_file2)
    f1 = open("text1.txt", "w")
    f2 = open("text2.txt", "w")
    f1.write(image_to_string(im1).encode('UTF=8'))
    f1.close()
    f2.write(image_to_string(im2).encode('UTF=8'))
    f2.close()
    text1 = open("text1.txt").read()
    text2 = open("text2.txt").read()
    m = SequenceMatcher(None, text1, text2)
    print m.ratio()
    return (m.ratio())

def mse(imageA, imageB):

    err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
    err /= float(imageA.shape[0] * imageA.shape[1])
    return err

def image_process(name):
    original = cv2.imread(name)
    contrast = cv2.imread("img_test_f.jpg")
    height1, width1 = contrast.shape[:2]
    height, width = original.shape[:2]

    if (height > height1) and (width > width1):
        original = cv2.resize(original, (width1, height1))
    else:
        contrast = cv2.resize(contrast, (width, height))

    original = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
    contrast = cv2.cvtColor(contrast, cv2.COLOR_BGR2GRAY)

    images = ("Original", original), ("Photoshopped", contrast)

    m = mse(original, contrast)
    print m
    return m

original="image_40.jpeg"
img=Image.open(original)
ocr_process(original)
image_process(original)