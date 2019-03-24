# Dyenhb папки cities создаём папку templates/cities, в которой будет храниться файл home.html
# c таким же содержимым, что и одноименный
from django.shortcuts import render

# импортируем класс DetailView
from django.views.generic.detail import DetailView

# добавляем класс CreateView для возможности создания нового отображения
from django.views.generic.edit import CreateView

# импортируем модель города
from .models import City

# ипортируем форму
from .forms import CityForm

# добавляем функциб reverse-lazy
from django.urls import reverse_lazy


# функция отображения

def home(request):
    # проверка данных, которые мы отправляем
    # если форма не заполнена, получаем сообщение
    if request.method == 'POST':
        form = CityForm(request.POST or None)
        # при попытке сохранить в форме уже существующие данные, print не сработает
        if form.is_valid():
            # печатаем, что получили из формы
            print(form.cleaned_data)
    form = CityForm()

    # отслеживаем куда ушёл запрос с формы, выводим только название города
    city = request.POST.get('name')
    # print(city)

    # запрос к базе  на получение всех записей; формируем html-ответ данными cities
    cities = City.objects.all()
    # форму так же  указываем в контексте, добавляем в словарь
    return render(request, 'cities/home.html', {'objects_list': cities, 'form': form})


# отображение страницы деталей для отдельной записи
class CityDetailView(DetailView):
    # обязательный параметр; ему задаются все записи(как и в похожей функции home), а он определяет, что конкретно
    # ему нужно
    queryset = City.objects.all()

    # задаём имя для контекста (c каким именем мы будем отпарвлять данные для рендеринга); по умолчания object

    context_object_name = 'object'

    # задаём имя шаблона

    template_name = 'cities/detail.html'


# отображение страницы создания новой записи
class CityCreateView(CreateView):
    # привязываем модель к City
    model = City

    # указываем форму класса
    form_class = CityForm

    # задаём имя шаблона

    template_name = 'cities/create.html'

    # функция возврата на домашнюю страницу(со списком городов) после успешного создания записи
    success_url = reverse_lazy('city:home')
