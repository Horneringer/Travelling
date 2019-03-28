from django.contrib import admin

from .models import Route

# регистрируем приложение Route в админке
admin.site.register(Route)

