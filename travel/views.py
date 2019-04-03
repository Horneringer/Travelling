from django.http import HttpResponse

# render более продвинутый метод
from django.shortcuts import render, redirect

# импортируем форму
from .forms import UserLoginForm

# импорт функций для входа и выхода
from django.contrib.auth import login, authenticate, logout


# функция отображения страницы приветствия, на запрос возвращает http-response
# функция render принимает запрос, шаблон(html файл) и словарь, где по ключу name подставляется соответствующее значение
def home_view(request):
    context = {'name': 'Щегол'}
    return render(request, 'home.html', context)


# функция входа в учетную запись
def login_view(request):
    form = UserLoginForm(request.POST or None)

    # следующим шагом после регистрации пользователь попадает на ту страницу, с которой он зашёл
    next_ = request.GET.get('next')

    # проверка валидности формы
    if form.is_valid():
        # получаем логин и пароль
        username = request.POST.get('username')
        password = request.POST.get('password')

        # аутентификация; метод strip позволяет очистить логин и пароль от возможных пробелов
        user = authenticate(username=username.strip(), password=password.strip())
        # функция входа в систему
        login(request, user)

        # получаем параметр из POST запроса
        next_post = request.POST.get('next')

        # в переменную записываем путь из GET или POST запроса
        # если пути отсутсвуют, то возвращается переход на главную страницу
        rederict_path = next_ or next_post or '/'
        return redirect(rederict_path)
    # возврат к форме авторизации, если она ещё не отрисована
    return render(request, 'login.html', {'form': form})


# функция выхода из учетной записи
def logout_view(request):
    logout(request)
    # переход на главную страницу
    return redirect('home')
