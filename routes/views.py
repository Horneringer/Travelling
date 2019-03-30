from django.shortcuts import render

from django.contrib import messages

# импорт модели Поезд
from trains.models import Train

# импортируем все формы
from .forms import *


# алгоритм обхода графа в глубину(поиск всех возможных путей из одного пункта в другой)
# в параметрах граф, представленный словарём(ключ - откуда, значения - куда можно добраться)

def dfs_paths(graph, start, goal):
    """ Вариант посещения одного и тогоже города более
    одного раза не рассматривается

    РАЗОБРАТЬСЯ КАК РАБОТАЕТ!
    """

    stack = [(start, [start])]
    while stack:
        vertex, path = stack.pop()
        if vertex in graph.keys():
            for next_ in graph[vertex] - set(path):
                if next_ == goal:
                    yield path + [next_]
                else:
                    stack.append((next_, path + [next_]))


# функция построения графа на основании записей из базы данных
def get_graph():
    # обращаемся к БД и получаем те города, откуда можно уехать(в качестве параметра задаём from_city)
    # в shell по данному запросу можно увидеть список словарей с ключом from_city и значением равным id города
    # (сколько было создано маршрутов в админке, столько словарей и будет) [{from_city:9},{from_city:11}]
    qs = Train.objects.values('from_city')

    # разворачиваем запрос, как генератор; через генератор разворачиваем список и делаем из него set
    # в итоге в переменной from_city_set будут храниться уникальные значения тех городов откуда можно выехать {9,11}
    from_city_set = set(i['from_city'] for i in qs)

    # создаём граф
    graph = {}
    for city in from_city_set:
        # по фильтру получаем список поездов с кконечными пунктами назначения
        # в shell можем увидеть список словарей с ключом to_city и id города в качестве значения
        trains = Train.objects.filter(from_city=city).values('to_city')

        # временный список
        tmp = set(i['to_city'] for i in trains)
        # в словаре graph создаём ключ city и значение tmp
        graph[city] = tmp

    # возвращаем порлученный граф
    return graph


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
