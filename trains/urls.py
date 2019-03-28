from django.urls import path
# добавляем функции и классы из файла отображения
from .views import home, TrainDetailView, TrainCreateView, TrainUpdateView, TrainDeleteView

# здесь добавляем адреса для функций и классов
urlpatterns = [

    path('detail/<int:pk>/', TrainDetailView.as_view(), name='detail'),
    path('update/<int:pk>/', TrainUpdateView.as_view(), name='update'),
    path('delete/<int:pk>/', TrainDeleteView.as_view(), name='delete'),
    path('add/', TrainCreateView.as_view(), name='add'),
    path('', home, name='home'),
]
