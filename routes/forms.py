from django import forms
from cities.models import City


# форма для маршрутов; будет привязана к модели Города
class RouteForm(forms.Form):
    from_city = forms.ModelChoiceField(label='Откуда', queryset=City.objects.all(),
                                       widget=forms.Select(attrs={'class': 'form-control', }))

    to_city = forms.ModelChoiceField(label='Куда', queryset=City.objects.all(),
                                     widget=forms.Select(attrs={'class': 'form-control', }))

    # поле 'через города'; осуществляется множественная выборка; поле будет необязательным для заполнения

    across_cities = forms.ModelMultipleChoiceField(label='Через города', queryset=City.objects.all(),
                                                   widget=forms.Select(attrs={'class': 'form-control', }),
                                                   required=False)

    traveling_time = forms.IntegerField(label='Время в пути', widget=forms.NumberInput(
        attrs={'class': 'form-control-sm', 'placeholder': 'Время в пути'}))
