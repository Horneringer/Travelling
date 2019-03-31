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
            # в data передаём первоначальные данные из формы
            data = form.cleaned_data

            # вызываем страницу с ошибкой и показываем те даные, которые мы отправляли в форме
            # !!! когда проект отправляется в продакшн, нужно обязательно указывать параметр DEBUG=FALSE,
            # чтобы скрыть данные в POST-запросе от (хацкеров например)!!!
            # assert False

            # передаем данные с ключами from_city, to_city, across_cities, traveling_time в соответствующие переменные
            from_city = data['from_city']
            to_city = data['to_city']
            across_cities_form = data['across_cities']
            traveling_time = data['traveling_time']

            # на основании этих данных можно построить граф и провести расчёт

            graph = get_graph()
            # записываем в переменную результат работы алгритма поиска
            # к параметрам dfs_path обращаемся через точку, так как они приходят из формы как объект города
            # получаем id города отправления и прибытия
            all_ways = list(dfs_paths(graph, from_city.id, to_city.id))

            # если маршруты отсутствуют

            if len(all_ways) == 0:
                messages.error(request, 'Маршрута не существует')
                # возврат на страницу с формой
                return render(request, 'routes/home.html', {'form': form})

            # проверка на наличие промежуточных городов(если была заполнена соответствующая строка в форме)
            if across_cities_form:
                # создаём список через генератор
                # в переменной across_cities будут id городов, через которые проходит заданный маршрут
                across_cities = [city.id for city in across_cities_form]

                # правильный путь
                right_ways = []

                # проверяем присутствует ли множество across_cities в множестве all_ways
                '''across_cities - список городов, через которые ХОЧЕТ проехать пользователь(он это указывает в форме)
                   all_ways - список городов, через которые МОЖНО проехать(список получаем по итогу работы алгоритмы поиска в глубину)'''

                for way in all_ways:
                    # если есть ПОЛНОЕ(потому что проверка all) совпадение
                    if all(point in way for point in across_cities):
                        # добавляем данный маршрут в список верных
                        right_ways = right_ways.append(way)
                    # если не нашли в существующих маршрутах ни одного , проходящего через нужные нам города

                if not right_ways:
                    # оповещение о том, что маршрут через заданные города невозможен
                    messages.error(request, 'Невозможно построить маршрут через заданные города!')
                    # возврат на страницу с формой
                    return render(request, 'routes/home.html', {'form': form})

            # если не указаны промежуточные города, записываем туда ВСЕ возможные варианты из алгоритма поиска
            else:
                right_ways = all_ways

            trains = []

            # обрабатываем каждый маршрут в списке right_ways
            # необходимо получить все поезда, которые ходят по каждому из маршрутов
            for route in right_ways:
                tmp = {}
                # список поездов для текущего маршрута
                tmp['trains'] = []

                # общее время пути
                total_time = 0
                # проходим по списку id, который задаёт маршрут
                for index in range(len(route) - 1):
                    # для этих id ищем соответствующий поезд
                    # делаем запрос, в качестве параметров укажем from_city - первый индекс, to_city - слудующий индекс(такая пара пунктов назначения задаёт поезд)
                    qs = Train.objects.filter(from_city=route[index], to_city=route[index + 1])

                    # если из одного города выходит несколько поездов и они отличаются только по времени
                    # необходимо получить поезд с меньшим временем; сортируем записи по параметру "время в пути"
                    # выбираем первый, если существует несколько одинаковых записей
                    qs = qs.order_by('travel_time').first()

                    # увеличиваем переменную, показывающую затраченное время
                    total_time += qs.travel_time
                    # добавляем поезд в список
                    tmp['trains'].append(qs)
                # перебрав все пересадки в маршруте, записываем для него общее время
                tmp['total_time'] = total_time

                # если полученное время маршрута меньше заданного,
                # то в итоговый список добавляем словарь с пересадками и общим временем на данном маршруте
                if total_time <= traveling_time:
                    trains.append(tmp)

            # если итоговый список поездов пуст
            if not trains:
                # выводим предупреждение
                messages.error(request, 'Время в пути больше выбранного!')
                #  и происходит возврат на страницу с формой
                return render(request, 'routes/home.html', {'form': form})

            routes = []

            cities = {'from_city': from_city.name, 'to_city': from_city.name}

            # модифицируем полученные данные в списке trains, чтобы улучшить отображение
            for tr in trains:
                # разворачиваем данные по каждому поезду в запись с несколькими полями(пересадки, общее время, откуда, куда)
                routes.append({'route': tr['trains'],
                               'total_time': tr['total_time'],
                               'from_city': from_city.name,
                               'to_city': to_city.name})

            # переменная, содержащая отсортированный список
            sorted_routes = []
            # если получили только один поезд в маршруте
            if routes == 1:
                sorted_routes = routes

            # если больше одного поезда в маршруте, то сортируем
            else:
                # делаем список из множества(если есть два маршрута с одинаковым временем, нет необходимости добавлять их все, а только один)
                # так мы получим список уникальных значений времени
                times = list(set(x['total_time'] for x in routes))
                # сортируем получившийся список по возрастанию времени
                times = sorted(times)

                # проходим по списку времени и списку маршрутов
                for time in times:
                    for route in routes:
                        # если время, которое мы получили в цикле равно времени внутри маршрута
                        if time == route['total_time']:
                            # данный маршрут добавляем в список sorted_routes, получим список отсортированных маршрутов
                            sorted_routes.append(route)

            context = {}

            form = RouteForm()
            # записываем в созданный словарь форму
            context['form'] = form

            # записываем список путей
            context['routes'] = sorted_routes

            context['cities'] = cities

            return render(request, 'routes/home.html', context)

            # возвращаем домашнюю страницу маршрутов
        return render(request, 'routes/home.html', {'form': form})

    # сообщение, если заданный маршрут не может быть найден

    else:
        messages.error(request, 'Создайте маршрут')
        # и снова отображаем страницу с формой
        form = RouteForm()
        return render(request, 'routes/home.html', {'form': form})
