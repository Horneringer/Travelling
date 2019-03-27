from django import forms

# импортируем модель Поезд
from .models import Train

from cities.models import City


# форма для поезда
class TrainForm(forms.ModelForm):
    name = forms.CharField(label='Поезд', widget=forms.TextInput(
        attrs={'class': 'form-control-sm', 'placeholder': 'Введите номер поезда'}))

    # переопределяем поля; данный тип поля позволяет сделать выбор из списка вариантов
    # список получаем с помощью querset
    # виджет для выбора - select
    from_city = forms.ModelChoiceField(label='Откуда', queryset=City.objects.all(),
                                       widget=forms.Select(attrs={'class': 'form-control-sm', 'placeholder': 'Откуда'}))

    to_city = forms.ModelChoiceField(label='Куда', queryset=City.objects.all(),
                                     widget=forms.Select(attrs={'class': 'form-control-sm', 'placeholder': 'Куда'}))

    travel_time = forms.IntegerField(label='Время в пути', widget=forms.NumberInput(
        attrs={'class': 'form-control-sm', 'placeholder': 'Время в пути'}))

    class Meta(object):
        model = Train
        # поля формы
        fields = ('name', 'from_city', 'to_city', 'travel_time')
