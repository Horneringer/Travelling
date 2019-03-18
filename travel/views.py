from django.http import HttpResponse

#render более продвинутый метод
from django.shortcuts import render


# функция отображения страницы приветствия, на запрос возвращает http-response
# функция render принимает запрос, шаблон(html файл) и словарь, где по ключу name подставляется соответствующее значение
def home_view(request):
    name = 'Зяблик'
    context = {'name': 'Щегол'}
    return render(request, 'home.html', context)
