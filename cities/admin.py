# Register your models here.
from django.contrib import admin
from .models import City

# регистрируем приложение City в админке
admin.site.register(City)
