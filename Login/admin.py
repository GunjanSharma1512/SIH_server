# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from .models import User, Images, davp_constraint

admin.site.register(User)
admin.site.register(Images)
admin.site.register(davp_constraint)
from .models import User, Images, davp_constraint, register
admin.site.register(register)