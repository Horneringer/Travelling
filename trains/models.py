# создаём модель Поезд
from django.db import models

# импортируем модель Город; так как паоезда ходят из городла в город, нужно всязать две модели

from cities.models import City


class Train(models.Model):
    # название поезда
    name = models.CharField(max_length=100, unique=True, verbose_name='Номер поезда')

    # откуда едет; отношение 'один ко многим'; в данном поле нужно указать ссылку на какой-либо город
    # в параметры передаём модель, к которой привязывается, on_delete - действие, которое применяется при удалении ссылочного объекта(города)
    # CASCADE - При удалении ссылочного объекта(города) также удаляются объекты, на которые есть ссылки(поезда)
    # related_name - имя по которому будут отличаться поля 'откуда' и 'куда' так как они оба ссылаются на одну модель City
    from_city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name='Откуда', related_name='from_city')

    # куда едет
    to_city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name='Куда', related_name='to_city')

    # время пути
    travel_time = models.IntegerField(verbose_name='Время в пути')

    class Meta:
        verbose_name = 'Поезд'
        verbose_name_plural = 'Поездa'
        ordering = ['name']

    # возвращает строку с инфой о номере поезда, начальной и конечной станции
    def __str__(self):
        return 'Поезд № {} из {} в {}'.format(self.name, self.from_city, self.to_city)
