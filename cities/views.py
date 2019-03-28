# Dyenhb папки cities создаём папку templates/cities, в которой будет храниться файл home.html
# c таким же содержимым, что и одноименный
from django.shortcuts import render

# импортируем класс DetailView для отображения деталей записи
from django.views.generic.detail import DetailView

# добавляем класс CreateView для возможности создания новой записи
from django.views.generic.edit import CreateView

# добавляем класс UpdateView для возможности редактирования записи
from django.views.generic.edit import UpdateView

# добавляем класс DeleteView для возможности удаления записи
from django.views.generic.edit import DeleteView

# импортируем пагинатор для разбиения на несколько страниц
from django.core.paginator import Paginator

# импортируем модель города
from .models import City

# ипортируем форму
from .forms import CityForm

# добавляем функциб reverse-lazy
from django.urls import reverse_lazy

# добавляем класс для отображения сообщений(миксин)
from django.contrib.messages.views import SuccessMessageMixin

from django.contrib import messages


# функция отображения домашней страницы

def home(request):
    # проверка данных, которые мы отправляем
    # если форма не заполнена, получаем сообщение

    """if request.method == 'POST':
        form = CityForm(request.POST or None)
        # при попытке сохранить в форме уже существующие данные, print не сработает
        if form.is_valid():
            # печатаем, что получили из формы
            print(form.cleaned_data)
    form = CityForm()

    # отслеживаем куда ушёл запрос с формы, выводим только название города
    city = request.POST.get('name')
    # print(city)"""

    # запрос к базе  на получение всех записей; формируем html-ответ данными cities
    cities = City.objects.all()
    # создаём объект класса Paginator;
    # в качестве параметров список всех записей и количество записей, отображаемых на одной странице
    paginator = Paginator(cities, 5)
    page = request.GET.get('page')
    cities = paginator.get_page(page)
    # форму так же  указываем в контексте, добавляем в словарь
    return render(request, 'cities/home.html', {'objects_list': cities, })


# отображение страницы деталей для отдельной записи
class CityDetailView(DetailView):
    # обязательный параметр; ему задаются все записи(как и в похожей функции home), а он определяет, что конкретно
    # ему нужно
    queryset = City.objects.all()

    # задаём имя для контекста (c каким именем мы будем отпарвлять данные для рендеринга); по умолчания object

    context_object_name = 'object'

    # задаём имя шаблона

    template_name = 'cities/detail.html'


# отображение страницы создания новой записи;
# созданный класс наследуется от миксина, который идёт обязательно ПЕРВЫМ параметром
class CityCreateView(SuccessMessageMixin, CreateView):
    # привязываем модель к City
    model = City

    # указываем форму класса
    form_class = CityForm

    # задаём имя шаблона

    template_name = 'cities/create.html'

    # функция возврата на домашнюю страницу(со списком городов) после успешного создания записи
    success_url = reverse_lazy('city:home')
    # сообщение об успешном завершении операции
    success_message = 'Город успешно добавлен!'


# отображение страницы изменения записи
class CityUpdateView(SuccessMessageMixin, UpdateView):
    # привязываем модель к City
    model = City

    # указываем форму класса
    form_class = CityForm

    # задаём имя шаблона

    template_name = 'cities/update.html'

    # функция возврата на домашнюю страницу(со списком городов) после успешного создания записи
    success_url = reverse_lazy('city:home')
    success_message = 'Внесенные изменения сохранены!'


# удаление записи; с удаление миксины не работают с шаблонами подтверждения? но работают несколько иначе с функцией ниже
class CityDeleteView(SuccessMessageMixin, DeleteView):
    model = City
    template_name = 'cities/delete.html'
    success_url = reverse_lazy('city:home')

    # если нет необходимости в подтверждении удаления, можно сделать так; без использования страницы подстверждения
    # cities/delete.html; так же иногда используется подтверждающий скрипт написанный на JS

    # def get(self, request, *args, **kwargs):
    #     messages.success(request, 'Город успешно удалён!')
    #     return self.post(request, request, *args, **kwargs)
