from django.urls import path
from .views import home, CityDetailView

# здесь добавляем адреса для функций и классов
urlpatterns = [
    # указываем первичный ключ(id) для записи; так как CityDetailView является классом, а не функцией, сделаем спец.
    # преобразование через as_view, дадим имя detail
    path('detail/<int:pk>/', CityDetailView.as_view(), name='detail'),
    path('', home, name='home'),
]
