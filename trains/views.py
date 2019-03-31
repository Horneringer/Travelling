from django.shortcuts import render

from .models import Train
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from django.core.paginator import Paginator
from django.contrib.messages.views import SuccessMessageMixin
from .forms import TrainForm
from django.urls import reverse_lazy
from django.contrib import messages


def home(request):
    trains = Train.objects.all()
    paginator = Paginator(trains, 10)
    page = request.GET.get('page')
    trains = paginator.get_page(page)
    # форму так же  указываем в контексте, добавляем в словарь
    return render(request, 'trains/home.html', {'objects_list': trains, })


class TrainDetailView(DetailView):

    queryset = Train.objects.all()

    # задаём имя для контекста (c каким именем мы будем отпрвлять данные для рендеринга); по умолчания object

    context_object_name = 'object'

    # задаём имя шаблона

    template_name = 'trains/detail.html'


class TrainCreateView(SuccessMessageMixin, CreateView):
    # привязываем модель к Train
    model = Train

    # указываем форму класса
    form_class = TrainForm

    # задаём имя шаблона

    template_name = 'trains/create.html'

    # функция возврата на домашнюю страницу(со списком поездов) после успешного создания записи
    success_url = reverse_lazy('train:home')
    # сообщение об успешном завершении операции
    success_message = 'Поезд успешно добавлен!'


class TrainUpdateView(SuccessMessageMixin, UpdateView):
    model = Train

    form_class = TrainForm

    template_name = 'trains/update.html'

    success_url = reverse_lazy('train:home')
    success_message = 'Внесенные изменения сохранены!'


class TrainDeleteView(DeleteView):
    model = Train
    template_name = 'trains/delete.html'
    success_url = reverse_lazy('train:home')

    # если нет необходимости в подтверждении удаления, можно сделать так; без использования страницы подстверждения
    # cities/delete.html; так же иногда используется подтверждающий скрипт написанный на JS

    # def get(self, request, *args, **kwargs):
    #     messages.success(request, 'Поезд успешно удалён!')
    #     return self.post(request, request, *args, **kwargs)
