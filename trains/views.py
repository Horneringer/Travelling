from django.shortcuts import render

from .models import Train
from django.core.paginator import Paginator


def home(request):
    trains = Train.objects.all()
    paginator = Paginator(trains, 5)
    page = request.GET.get('page')
    trains = paginator.get_page(page)
    # форму так же  указываем в контексте, добавляем в словарь
    return render(request, 'trains/home.html', {'objects_list': trains, })
