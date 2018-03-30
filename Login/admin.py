# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from .models import User, Image, davp_constraint

admin.site.register(User)
admin.site.register(Image)
admin.site.register(davp_constraint)
from .models import User, Image, davp_constraint, register
admin.site.register(register)