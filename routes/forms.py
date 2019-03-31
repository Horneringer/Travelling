from django import forms
from cities.models import City


# форма для маршрутов; будет привязана к модели Города
# добавляем классы из JS для работы select 2 в формах(одиночных и множественных)
# классы находятся в скриптах в base.html
class RouteForm(forms.Form):
    from_city = forms.ModelChoiceField(label='Откуда', queryset=City.objects.all(),
                                       widget=forms.Select(attrs={'class': 'form-control js-example-basic-single', }))

    to_city = forms.ModelChoiceField(label='Куда', queryset=City.objects.all(),
                                     widget=forms.Select(attrs={'class': 'form-control js-example-basic-single', }))

    # поле 'через города'; осуществляется множественная выборка; поле будет необязательным для заполнения;
    # SelectMultiple позволяет выбирать несколько варантов для заполнения одного поля

    across_cities = forms.ModelMultipleChoiceField(label='Через города', queryset=City.objects.all(),
                                                   widget=forms.SelectMultiple(attrs={'class': 'form-control js-example-basic-multiple', }),
                                                   required=False)

    traveling_time = forms.IntegerField(label='Время в пути', widget=forms.NumberInput(
        attrs={'class': 'form-control', 'placeholder': 'Время в пути'}))
