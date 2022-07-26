from braces.views import AnonymousRequiredMixin

from django.shortcuts import render
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    CreateView, FormView, ListView, DetailView,
)

from courses.models import Course
from students.forms import RegistrationModelForm, CourseEnrollForm

from common.analize.analizetools import (
    p_dir, p_mro, p_glob, p_loc, p_type,
    delimiter, p_content, show_builtins,
    show_doc, console, console_compose,
)


class StudentRegistrationView(AnonymousRequiredMixin, CreateView):
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

    def get_authenticated_redirect_url(self):
        user = self.request.user
        if user.is_superuser or user.has_perm('courses.add_course'):
            return reverse_lazy('courses:manage_course_list')
        return reverse_lazy('courses:course_list')


class StudentEnrollCourseView(LoginRequiredMixin, FormView):
    form_class = CourseEnrollForm

    def form_valid(self, form):
        cd = form.cleaned_data
        self.course = cd['course']

        # --- console ---
        console(cd)
        console(self.request.POST)
        # --- console ---

        self.course.students.add(self.request.user)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('students:student_course_detail', kwargs={
            'slug': self.course.slug,
        })


class StudentCourseListView(LoginRequiredMixin, ListView):
    model = Course
    template_name = 'students/course/list.html'

    def get_queryset(self):
        return super().get_queryset().filter(students__in=[self.request.user, ])


class StudentCourseDetailView(LoginRequiredMixin, DetailView):
    model = Course
    template_name = 'students/course/detail.html'

    def get_queryset(self):
        return super().get_queryset().filter(
            students__in=[self.request.user, ]
        ).prefetch_related('modules')

    def get_context_data(self, **kwargs):
        ctx = super(StudentCourseDetailView, self).get_context_data(**kwargs)
        course = self.get_object()
        if 'module_id' in self.kwargs:
            module = course.modules.get(pk=self.kwargs['module_id'])
        else:
            module = course.modules.all()[0]
        ctx['module'] = module
        return ctx


def empty_view(request):
    return JsonResponse({'status': 'ok', })
