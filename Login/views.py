# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import decimal

import thread
import time

from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from rest_framework.decorators import api_view, permission_classes
from rest_framework import generics, permissions
from models import User,Images,davp_constraint,register
from rest_framework.response import Response
from django.core.files import File
import numpy as np
import cv2
import django.core.files
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
import smtplib
import requests
import json
from django.core.mail import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import random
import base64
import struct
import hashlib
from django.views.decorators.csrf import csrf_exempt
from geopy.geocoders import Nominatim
import os
from PIL import Image
import PIL.Image
from pytesseract import *
from difflib import SequenceMatcher


# Create your views here.
@csrf_exempt
@api_view(['GET', 'POST'])
@permission_classes((permissions.AllowAny,))
# Checks user registration
def checkmatch(request):
    if request.method == 'POST':
        id = request.POST.get('user')
        pwd = request.POST.get('pass')
        try:
            checkuser = User.objects.get(user=id)
        except ObjectDoesNotExist:
            checkuser = None

        if checkuser is not None:
            if pwd == checkuser.password:
                response_data = {}
                response_data['id'] = checkuser.id
              #  print response_data
                return Response(response_data)
            else:
                return Response("nomatch")


        else:
            return Response("nouser")


@api_view(['GET', 'POST'])
@permission_classes((permissions.AllowAny,))
#submits the user data in a database
def unhash(request):
    if request.method == 'POST':
        photo=request.POST.get('photo')
        hashcode=request.POST.get('hashcode')
        encrypted=request.POST.get('encrypted')
        #caption is added
        caption=request.POST.get('caption')

        list = encrypted.split("_")
        print list

        #storing the geo-tagged information in variables

        lat=list[0]
        long=list[1]
        hr=list[2]
        min=list[3]
        day=list[4]
        month=list[5]
        yr=list[6]

        hard_location="Jagatpura, Jaipur Municipal Corporation, Jaipur, Rajasthan, 302033, India"

        # forming the address and storing it in variable

        list.pop(2)
        list.pop(2)
        list.pop(2)
        list.pop(2)
        list.pop(2)
        try:
            geolocator = Nominatim()
            location = geolocator.reverse(list)

            address= (location.address)
        except:
            address=hard_location
        # saving the image in jpeg file

        image = open("image.jpeg", "wb")
        image.write(photo.decode('base64'))
        image.close()
        #generate the hash of the image
        #hash = hashlib.md5()
        hash = hashlib.sha256()
        print hash
        hash.update(open('image.jpeg', 'rb').read())

        generated_hash=(hash.digest()).encode('base64')

        user_obj = Images()


        # saving into database

        user_obj.hashcode=hashcode
        user_obj.caption = caption
        user_obj.latitude = lat
        user_obj.longitude = long
        user_obj.date = day
        user_obj.month = month
        user_obj.year = yr
        user_obj.ocr = 1
        user_obj.mse = 1
        user_obj.pic.save('image.jpeg', File(open('image.jpeg')),save=False)

        user_obj.location=address
        user_obj.generated_hash=generated_hash
        user_obj.save(force_insert=True)

        #ocr = ocr_process('image.jpeg')
        #mse = image_process('image.jpeg')
        #user_obj.ocr = ocr
        #user_obj.mse = mse
        #user_obj.save()
        ##########
        global new_name

        new_name = str("image_" + str(user_obj.Uid) + ".jpeg")
        os.rename("image.jpeg",new_name)
        new_name2="image_"+str(user_obj.Uid)
        new_name.encode('UTF-8')


        #returning the user id of the data user submitted
        print(user_obj.Uid)

        try:
            #thread.start_new_thread(return_Uid, ("Thread-1",user_obj.Uid,))
            thread.start_new_thread(constraint_match, ("Thread-2",user_obj.Uid,))
        except Exception as e:
            print (e)
        return Response(user_obj.Uid)

def return_Uid(name,id):
    print("returned from return_Uid")
    return Response(id)



def less_than_equal(a, b, epsilon=1e-3):
    return abs(a-b)<=2*epsilon

def greater_than_equal(a, b, epsilon=1e-3):
    return abs(a-b)>=2*epsilon



#Matches the constraints specified by davp to validate data
#@csrf_exempt
#@api_view(['GET', 'POST'])
#@permission_classes((permissions.AllowAny,))
def constraint_match(name,mid):
    #if request.method=='POST':
        #mid=request.POST.get('id')
        #search the Image stored with the help of the id

        try:
            user = Images.objects.get(Uid=mid)
        except ObjectDoesNotExist:
            user = None
        #if no such image was stored
        if user is None:
            return Response("data not found")

        else:
            ok_response = "matched"
            not_ok = "not matched"
            warning_response="warning"
            print("here1")
            #if hash generated was same as then one user sent
            if user.generated_hash == user.hashcode:

                lat=user.latitude
                long=user.longitude
                day=user.date
                month=user.month
                year=user.year

                print("here2")

                #search through all objects defined by davp database and check if any constraint matches

                for obj in davp_constraint.objects.all():
                  #  if less_than_equal(lat, obj.latitude)  and less_than_equal(long, obj.longitude):
                  if lat>=(obj.latitude-decimal.Decimal(0.222)) and lat<=(obj.latitude+decimal.Decimal(0.222)) and long>=(obj.longitude-decimal.Decimal(0.222)) and long<=(obj.longitude+decimal.Decimal(0.222)):
                    print("here4")
                    print(str(day)+" "+str(month)+" "+str(year))
                  #  if day >= obj.s_date and day <= obj.e_date and month >= obj.s_month and month <= obj.e_month and year >= obj.s_year and year <= obj.e_year:
                    if checkDate(obj.s_date,obj.e_date,obj.s_month,obj.e_month,obj.s_year,obj.e_year,day,month,year):
                            print("yes")
                            global new_name
                            ocr=ocr_process(str(new_name))
                            mse=image_process(str(new_name))
                            #print type(new_name+".jpeg")
                            #print(new_name+"hi")

                            if ocr>=decimal.Decimal(0.3) and mse<=1000:
                                return HttpResponse(ok_response)
                            else:
                                return HttpResponse(warning_response)

                   # if lat>=(obj.latitude-0.002) and lat<=(obj.latitude+0.002) and long>=(obj.longitude-0.002) and long<=(obj.longitude+0.002):
                    #    if day>=obj.s_date and day<=obj.e_date and month>=obj.s_month and month<=obj.e_month and year>=obj.s_year and year<=obj.e_year:
                     #       return Response("matched")
                print("here3")
                return HttpResponse(not_ok)
            else:
                print("here4")
                return HttpResponse(not_ok)


def checkDate(s_date,e_date,s_month,e_month,s_year,e_year,date,month,year):
    if year>=s_year and year<=e_year:
        if month>=s_month and month<=e_month:
            if s_date<=e_date:
                if s_month==e_month:
                    if date>=s_date and date<=e_date:
                        return (True)
                else:
                    if (date>=s_date and date<=31) or (date>=1 and date<=e_date):
                        return True
            elif s_date>e_date:
                if (date>=s_date and date<=31) or (date<=e_date and date>=1):
                    return (True)
    return False

@csrf_exempt
@api_view(['GET', 'POST'])
@permission_classes((permissions.AllowAny,))
def registerit(request):
    if request.method == 'POST':
        agency= request.POST.get('agency')
        add = request.POST.get('add')
        contact = request.POST.get('contact')
        email = request.POST.get('email')
        pas = request.POST.get('pass')

        obj = register()
        obj.agency = agency
        obj.add= add
        obj.contact= contact
        obj.email= email
        obj.pas= pas
        obj.save()
        return Response("successful")

def ocr_process(image_file1):
    #image_file1 = 'IMG_TEST6.jpg'
    image_file2 = 'img_test_f.jpg'
    img2 = PIL.Image.open(image_file2)

    im1 = PIL.Image.open(image_file1)
    im2 = PIL.Image.open(image_file2)
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

new_name=""
