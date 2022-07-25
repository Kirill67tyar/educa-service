from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth import authenticate, login

from students.forms import RegistrationModelForm


class StudentRegistrationView(CreateView):
    form_class = RegistrationModelForm
    success_url = reverse_lazy('students:empty')
    template_name = 'students/student/registration.html'

    # метод класса CreateView, вызывается если форма была валидна
    # есть ещё form_invalid(self, form)
    # метод должен возвращать объект HTTP-ответа
    def form_valid(self, form):
        result = super().form_valid(form)
        cd = form.cleaned_data
        user = authenticate(
            request=self.request,
            username=cd['username'],
            password=cd['password']
        )
        # с помощью функции login() создаём сессионный ключ, который сохраняется в таблицу django_session
        # в столбик session_key (VARCHAR) передаётся в загловке HTTP ответа - Set-Cookie
        # и сохраняется у клиента в браузере в куках
        login(
            request=self.request,
            user=user,
        )
        return result


def empty_view(request):
    return JsonResponse({'status': 'ok', })
