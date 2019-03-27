from django.urls import path
# добавляем функции и классы из файла отображения
from .views import (home, )

# здесь добавляем адреса для функций и классов
urlpatterns = [
    # указываем первичный ключ(id) для записи; так как CityDetailView и CityCreateView являются классами,
    # а не функцией, сделаем спец. преобразование через as_view, дадим имена (detail, add)
    # path('detail/<int:pk>/', CityDetailView.as_view(), name='detail'),
    # path('add/', CityCreateView.as_view(), name='add'),
    # по первичному ключу выбираем какую конкртно запись нужно редактировать
    # path('update/<int:pk>/', CityUpdateView.as_view(), name='update'),
    # path('delete/<int:pk>/', CityDeleteView.as_view(), name='delete'),

    path('', home, name='home'),
]
