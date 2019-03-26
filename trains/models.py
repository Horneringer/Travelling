# создаём модель Поезд
from django.db import models

# импортируем модель Город; так как паоезда ходят из городла в город, нужно всязать две модели

from cities.models import City

# импортируем библиотеку для работы с исключениями
from django.core.exceptions import ValidationError


class Train(models.Model):
    # название поезда
    name = models.CharField(max_length=100, unique=True, verbose_name='Номер поезда')

    # откуда едет;
    # отношение 'один ко многим'; в данном поле нужно указать ссылку на какой-либо город
    # в параметры передаём модель, к которой привязывается, on_delete - действие, которое применяется при удалении ссылочного объекта(города)
    # CASCADE - при удалении ссылочного объекта(города) также удаляются объекты, на которые есть ссылки(поезда)
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

    # функция проверки валидности введненных в форму данных
    def clean(self, *args, **kwargs):
        # проверка на совпадение пунктов начначения
        if self.from_city == self.to_city:
            raise ValidationError('Измените город отправления/прибытия')
        # проверяем не существует ли уже задаваемого маршрута(пункты и время)
        # обращаемяся к записям базы данных;
        # чтобы не возникала ошибка во время редактирования записи, исключаем запись из запроса по первичному ключу
        qs = Train.objects.filter(from_city=self.from_city, to_city=self.to_city, travel_time=self.travel_time).exclude(
            pk=self.pk)

        # если запись уже существует, выкидываем ошибку и просим изменить время пути
        if qs.exists():
            raise ValidationError('Измените время пути')
        # прочитать про super
        return super(Train, self).clean(*args, **kwargs) 
