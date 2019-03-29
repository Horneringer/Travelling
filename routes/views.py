from django.shortcuts import render

from django.contrib import messages

# импортируем все формы
from .forms import *


# функция отображения домашней страницы маршрутов
def home(request):
    form = RouteForm()
    return render(request, 'routes/home.html', {'form': form})


# функция поиска маршрутов
# функция будет работать только тогда , когда мы получим нашу форму поиска для обработки
# иначе пользователь получает сообщение о необходимости заполнинть форму

def find_routes(request):
    if request.method == 'POST':
        # обработка формы
        form = RouteForm(request.POST or None)
        # проверка валидности формы
        if form.is_valid():
            # в data передаём данные из формы
            data = form.changed_data

            # вызываем страницу с ошибкой и показываем те даные, которые мы отправляли в форме
            # !!! когда проект отправляется в продакшн, нужно обязательно указывать параметр DEBUG=FALSE,
            # чтобы скрыть данные в POST-запросе от (хацкеров например)!!!
            assert False

            # возвращаем домашнюю страницу маршрутов
        return render(request, 'routes/home.html', {'form': form})

    # сообщение, если заданный маршрут не может быть найден

    else:
        messages.error(request, 'Создайте маршрут')
        # и снова отображаем страницу с формой
        form = RouteForm()
        return render(request, 'routes/home.html', {'form': form})
