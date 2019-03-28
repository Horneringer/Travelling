# файл для форм

# импортируем формы
from django import forms

# импортируем модель, к которой привяжем форму
from .models import City


class HtmlForm(forms.Form):
    # определение типа полей
    name = forms.CharField(label='Город')


class CityForm(forms.ModelForm):
    # добавляем виджет с необходимыми атрибутами и плейсхолдер -- надпись-подсказка внутри формы; таким образом мы
    # передадим форме оформление
    name = forms.CharField(label='Город', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Введите название города'}))

    class Meta(object):
        # задаём модель
        model = City
        # указываем в fields поля, которые будут в форме
        fields = ('name',)
