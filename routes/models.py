from django.db import models

# импортируем модель Поезд
from trains.models import Train


# класс Маршрут
class Route(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название маршрута', unique=True)

    from_city = models.CharField(max_length=100, verbose_name='Откуда')
    to_city = models.CharField(max_length=100, verbose_name='Куда')

    # через какие города проходит маршрут;
    # отношение "многие ко многим", в параметрах указываем модель,
    # при blank=True, проверка данных в форме позволит сохранять пустое значение в поле(если вдруг промежуточных городов нет), при blank=False поле будет обязательным.
    across_cities = models.ManyToManyField(Train, blank=True, verbose_name='Через города')
    travev_times = models.IntegerField(verbose_name='Время в пути')


# возврат названия маршрута
def __str__(self):
    return self.name


class Meta:
    verbose_name = 'Маршрут'
    verbose_name_plural = 'Маршруты'
    ordering = ['name']
