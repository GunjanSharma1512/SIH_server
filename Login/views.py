# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import decimal

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
import os

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
        #caption=request.POST.get('caption')

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
        hash = hashlib.md5()
        hash.update(open('image.jpeg', 'rb').read())

        generated_hash=(hash.digest()).encode('base64')

        #saving into database
        user_obj = Image()
        ##########3
        user_obj.hashcode=hashcode
        #user_obj.caption = caption
        user_obj.latitude = lat
        user_obj.longitude = long
        user_obj.date = day
        user_obj.month = month
        user_obj.year = yr
        #user_obj.pic = "image.jpeg"
        #user_obj.pic.save("image.jpeg", django_file, save=True)
        user_obj.pic.save('image.jpeg', File(open('image.jpeg')),save=False)

        user_obj.location=address
        user_obj.generated_hash=generated_hash
        user_obj.save(force_insert=True)
        new_name="image_"+str(user_obj.Uid)+".jpeg"
        os.rename("image.jpeg",new_name)

        #returning the user id of the data user submitted
        print(user_obj.Uid)
        return Response(user_obj.Uid)



def less_than_equal(a, b, epsilon=1e-3):
    return abs(a-b)<=2*epsilon

def greater_than_equal(a, b, epsilon=1e-3):
    return abs(a-b)>=2*epsilon



#Matches the constraints specified by davp to validate data
@csrf_exempt
@api_view(['GET', 'POST'])
@permission_classes((permissions.AllowAny,))
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
            ok_response = "matched"
            not_ok = "not matched"
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
                  if lat>=(obj.latitude-decimal.Decimal(0.002)) and lat<=(obj.latitude+decimal.Decimal(0.002)) and long>=(obj.longitude-decimal.Decimal(0.002)) and long<=(obj.longitude+decimal.Decimal(0.002)):
                    print("here4")
                    print(str(day)+" "+str(month)+" "+str(year))
                  #  if day >= obj.s_date and day <= obj.e_date and month >= obj.s_month and month <= obj.e_month and year >= obj.s_year and year <= obj.e_year:
                    if checkDate(obj.s_date,obj.e_date,obj.s_month,obj.e_month,obj.s_year,obj.e_year,day,month,year):
                            print("yes")
                            return HttpResponse(ok_response)
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


