# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from rest_framework.decorators import api_view, permission_classes
from rest_framework import generics, permissions
from models import User,Image,davp_constraint
from rest_framework.response import Response
from django.core.files import File

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

        # forming the address and storing it in variable

        list.pop(2)
        list.pop(2)
        list.pop(2)
        list.pop(2)
        list.pop(2)
        geolocator = Nominatim()
        location = geolocator.reverse(list)

        address= (location.address)


        #image.close()

        #generate the hash of the image
        hash = hashlib.md5()
        hash.update(open('image.jpeg', 'rb').read())

        generated_hash=(hash.digest()).encode('base64')

        #saving into database
        user_obj = Image()
        user_obj.hashcode=hashcode
        user_obj.caption = caption
        user_obj.latitude = lat
        user_obj.longitude = long
        user_obj.date = day
        user_obj.month = month
        user_obj.year = yr
        #user_obj.pic="image.jpeg"

        # saving the image in jpeg file

        image = open("image.jpeg", "wb")
        image.write(photo.decode('base64'))

        django_file = File(image)
        user_obj.pic.save("image.jpeg", django_file, save=True)
        image.close()

        user_obj.location=address
        user_obj.generated_hash=generated_hash
        user_obj.save(force_insert=True)

        #returning the user id of the data user submitted
        return Response(user_obj.Uid)



#Matches the constraints specified by davp to validate data
def constraint_match(request):
    if request.method=='POST':
        mid=request.POST.get('id')
        #search the Image stored with the help of the id
        try:
            user = Image.objects.get(Uid=mid)
        except ObjectDoesNotExist:
            user = None
        #if no such image was stored
        if user is None:
            return Response("data not found")

        else:
            #if hash generated was same as then one user sent
            if user.generated_hash == user.hashcode:

                lat=user.latitude
                long=user.longitude
                day=user.date
                month=user.month
                year=user.year

                #search through all objects defined by davp database and check if any constraint matches

                for obj in davp_constraint.objects.get():
                    if lat>=(obj.latitude-0.002) and lat<=(obj.latitude+0.002) and long>=(obj.longitude-0.002) and long<=(obj.longitude+0.002):
                        if day>=obj.s_date and day<=obj.e_date and month>=obj.s_month and month<=obj.e_month and year>=obj.s_year and year<=obj.e_year:
                            return Response("matched")
                return Response("not matched")
            else:
                return Response("not matched")





