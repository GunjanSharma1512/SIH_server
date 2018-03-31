from __future__ import unicode_literals

from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=100)

    def __unicode__(self):
        return self.email

    def as_json(self):
        return dict(
            name=self.name,
            email=self.email,
            password=self.password,
        )

#model to store the image as sent by the user including all it's details
class Images(models.Model):
    Uid=models.AutoField(primary_key=True)

    caption=  models.CharField(max_length=200)

    pic = models.ImageField(upload_to="images")
    #pic = models.FileField()

    latitude = models.DecimalField(max_digits=1000, decimal_places=40)
    longitude = models.DecimalField(max_digits=1000, decimal_places=40)
    location =  models.CharField(max_length=300)

    date = models.IntegerField()
    month = models.IntegerField()
    year =models.IntegerField()
    hashcode =models.CharField(max_length=200)
    generated_hash =models.CharField(max_length=200)
    ocr=models.DecimalField(max_digits=1000, decimal_places=40)
    mse=models.DecimalField(max_digits=1000, decimal_places=40)





    def as_json(self):
        return dict(
            caption= self.caption,
            date = self.date,
            month = self.month,
            year = self.year,
        )
#model to store the constraints specified by davp
class davp_constraint(models.Model):
    latitude = models.DecimalField(max_digits=1000, decimal_places=40)
    longitude = models.DecimalField(max_digits=1000, decimal_places=40)
    s_date = models.IntegerField()
    s_month = models.IntegerField()
    s_year = models.IntegerField()
    e_date = models.IntegerField()
    e_month = models.IntegerField()
    e_year = models.IntegerField()

class register(models.Model):
    agency = models.CharField(max_length=100)
    add = models.CharField(max_length= 200)
    contact= models.IntegerField()
    email= models.EmailField()
    pas= models.CharField(max_length = 50)


    def __unicode__(self):
        return self.email
    def as_json(self):
        return dict(
            name=self.agency,
            email=self.add,
            contact=self.contact,
            pas= self.pas
        )
