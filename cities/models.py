from django.db import models


# каждый класс в models.py это отдельная таблица для базы данных; при создании миграций прописывается в файле
# /migrations/initial.py(id создается всегда автоматически с типом поля autoField)
class City(models.Model):
    # поле name будет содержать данный типа char длинной не более 100 символов; делаем данное название уникальным
    # в 3-м параметре указываем название поля непосредственно на странице сайта
    name = models.CharField(max_length=100, unique=True, verbose_name='Город')

    # функция возвращает название города в качестве имени объекта класса City(вместо City object)
    def __str__(self):
        return self.name

    # для отдельного поля будет имя поля 'Город', все поля будут с название города (вместо непонятного Citys)
    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'
        # сортировка списка городов, в данном случае по имени
        ordering = ['name']
