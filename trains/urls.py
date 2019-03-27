from django.urls import path
# добавляем функции и классы из файла отображения
from .views import home, TrainCreateView, TrainUpdateView, TrainDeleteView

# здесь добавляем адреса для функций и классов
urlpatterns = [

    # path('detail/<int:pk>/', CityDetailView.as_view(), name='detail'),
    path('add/', TrainCreateView.as_view(), name='add'),

    # по первичному ключу выбираем какую конкртно запись нужно редактировать
    path('update/<int:pk>/', TrainUpdateView.as_view(), name='update'),
    path('delete/<int:pk>/', TrainDeleteView.as_view(), name='delete'),
    path('', home, name='home'),
]
