# Dyenhb папки cities создаём папку templates/cities, в которой будет храниться файл home.html
# c таким же содержимым, что и одноименный
from django.shortcuts import render

# импортируем класс DetailView
from django.views.generic.detail import DetailView

# импортируем модель города
from .models import City


# функция отображения

def home(request):
    # запрос к базе  на получение всех записей; формируем html-ответ данными cities
    cities = City.objects.all()
    return render(request, 'cities/home.html', {'objects_list': cities})


class CityDetailView(DetailView):
    # обязательный параметр; ему задаются все записи(как и в похожей функции home), а он определяет, что конкретно
    # ему нужно
    queryset = City.objects.all()

    # задаём имя для контекста; по умолчания object

    context_object_name = 'object'

    # задаём имя шаблона

    template_name = 'cities/detail.html'
