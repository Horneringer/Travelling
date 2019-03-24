# Dyenhb папки cities создаём папку templates/cities, в которой будет храниться файл home.html
# c таким же содержимым, что и одноименный
from django.shortcuts import render

# импортируем класс DetailView
from django.views.generic.detail import DetailView

# импортируем модель города
from .models import City

# ипортируем форму
from .forms import HtmlForm


# функция отображения

def home(request):
    # проверка данных, которые мы отправляем
    # если форма не заполнена, получаем сообщение
    if request.method == 'POST':
        form = HtmlForm(request.POST or None)
        if form.is_valid():
            # печатаем, что получили из формы
            print(form.cleaned_data)
    form = HtmlForm()

    # отслеживаем куда ушёл запрос с формы, выводим только название города
    city = request.POST.get('name')
    # print(city)

    # запрос к базе  на получение всех записей; формируем html-ответ данными cities
    cities = City.objects.all()
    # форму так же  указываем в контексте, добавляем в словарь
    return render(request, 'cities/home.html', {'objects_list': cities, 'form': form})


class CityDetailView(DetailView):
    # обязательный параметр; ему задаются все записи(как и в похожей функции home), а он определяет, что конкретно
    # ему нужно
    queryset = City.objects.all()

    # задаём имя для контекста (c каким именем мы будем отпарвлять данные для рендеринга); по умолчания object

    context_object_name = 'object'

    # задаём имя шаблона

    template_name = 'cities/detail.html'
