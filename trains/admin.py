from django.contrib import admin
from .models import Train


# класс для кастомизации админки в приложения Поезда
class TrainAdmin(admin.ModelAdmin):
    class Meta:
        model = Train

    # в list_display указываем все поля, которые нужны для отображения в админке
    list_display = ('name', 'from_city', 'to_city', 'travel_time')
    # метод позволяет на странице отображение редактировать поле
    list_editable = ['travel_time']


# регистрируем приложение Train в админке
admin.site.register(Train, TrainAdmin)
