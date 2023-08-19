from django.contrib import admin

from .models import Departments, Profile, Company

admin.site.register(Departments)
admin.site.register(Profile)
admin.site.register(Company)