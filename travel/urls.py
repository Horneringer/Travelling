"""travel URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

# общий url для всего проекта
from django.contrib import admin
from django.urls import path, include
from routes.views import home, find_routes, add_route

urlpatterns = [
    # адрес админки
    path('admin/', admin.site.urls),

    # адрес приложения Города
    # прописываем путь для url, находящегося в cities с помощью функции include;
    # в качестве аргументов указываем директорию и пространство имён
    path('cities/', include(('cities.urls', 'city'))),

    # адрес приложения Поезда
    path('trains/', include(('trains.urls', 'train'))),

    # адрес страницы с найденными маршрутами
    path('find/', find_routes, name='find_routes'),

    # адресс с сохраненными маршрутами
    path('add_route/', add_route, name='add_route'),

    # адрес приложения Маршруты
    # форма поиска маршрутов будет отображаться на главной странице
    path('', home, name='home'),
]
