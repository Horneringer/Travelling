# файл для форм

# импортируем формы
from django import forms


class HtmlForm(forms.Form):
    # определение типа полей
    name = forms.CharField(label='Город')
