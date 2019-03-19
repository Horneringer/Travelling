# Dyenhb папки cities создаём папку templates/cities, в которой будет храниться файл home.html
# c таким же содержимым, что и одноименный
from django.shortcuts import render

# импортируем модель города
from .models import City


# функция отображения

def home(request):
    # запрос к базе  на получение всех записей; формируем html-ответ данными cities
    cities = City.objects.all()
    return render(request, 'cities/home.html', {'objects_list':cities})