from django.shortcuts import render

# импортируем все формы
from .forms import *


# функция отображения домашней страницы маршрутов
def home(request):
    form = RouteForm()
    return render(request, 'routes/home.html', {'form': form})
