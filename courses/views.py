from django.shortcuts import (
    redirect, render, get_object_or_404,
)
from django.urls import reverse_lazy
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
)
from django.views.generic import (
    View, ListView, CreateView,
    UpdateView, DetailView, DeleteView,
)
from django.views.generic.base import TemplateResponseMixin

from courses.forms import ModuleFormSet
from courses.models import (
    Subject, Course,
    Module, Content,
)


class OwnerMixin:
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(owner=self.request.user)
        # return self.model.objects.filter(owner=self.request.user)


class OwnerEditMixin:
    # для ModelFormMixin, который работает с формами
    # (от него наследованы CreateView и UpdateView)
    # form_valid выполняется когда форма успешно проходит валидацию
    def form_valid(self, form):
        try:
            form.instance.owner = self.request.user
        except AttributeError:
            pass
        return super().form_valid(form)


class OwnerCourseMixin(OwnerMixin, LoginRequiredMixin):
    model = Course
    fields = [
        'subject', 'title', 'description',  # 'slug',
    ]
    success_url = reverse_lazy('courses:manage_course_list')

    # можно убрать наследование от OwnerMixin, потому что он дальше
    # нигде не используется
    # def get_queryset(self):
    #     qs = super().get_queryset()
    #     return qs.filter(owner=self.request.user)
    #     # return self.model.objects.filter(owner=self.request.user)


class OwnerCourseEditMixin(OwnerCourseMixin, OwnerEditMixin):
    # fields = [
    #     'subject', 'title', 'description',  # 'slug',
    # ]
    # success_url = reverse_lazy('courses:manage_course_list')
    template_name = 'courses/form.html'


class ManageCourseListView(OwnerCourseMixin, ListView):
    template_name = 'courses/list.html'


class CourseCreateView(PermissionRequiredMixin, OwnerCourseEditMixin, CreateView):
    permission_required = 'courses.add_course'


class CourseUpdateView(PermissionRequiredMixin, OwnerCourseEditMixin, UpdateView):
    permission_required = 'courses.update_course'


class CourseDeleteView(PermissionRequiredMixin, OwnerCourseMixin, DeleteView):
    template_name = 'courses/delete.html'
    success_url = reverse_lazy('courses:manage_course_list')
    permission_required = 'courses.delete_course'

    # # как удалить сразу без перехода на страницу delete.html
    # # DeleteView удаляет только при Post запросе
    # template_name = None
    # def get(self, request, *args, **kwargs):
    #     return self.post(request, *args, **kwargs)


class CourseModuleUpdateView(TemplateResponseMixin, View):
    template_name = 'courses/manage/module/formset.html'
    course = None

    def get_formset(self, data=None):  # что бы избежать дублирования
        return ModuleFormSet(data=data, instance=self.course)

    def dispatch(self, request, pk, *args, **kwargs):
        """
            вызывает дальше self.get или self.post, взависимости
            от того какой метод HTTP запроса
        """
        self.course = get_object_or_404(
            klass=Course,
            pk=pk,
            owner=request.user
        )
        return super().dispatch(request, pk, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        formset = self.get_formset()
        return self.render_to_response(  # метод от TemplateResponseMixin (можно просто передать контекст)
            context={
                'formset': formset,
                'course': self.course,
            }
        )

    def post(self, request, *args, **kwargs):
        formset = self.get_formset(data=request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('courses:manage_course_list')
        return self.render_to_response(
            context={
                'formset': formset,
                'course': self.course,
            }
        )


"""
CourseModuleUpdateView 
унаследован от: TemplateResponseMixin View

TemplateResponseMixin - примесь, которая добавит формирование HTML шаблона
и вернет его в качестве ответа на запрос.

Использует шаблон template_name определенный как атрибут класса. 
Добавляет в дочерние классы метод render_to_response
в который можно просто передать контекст и он будет использовать template_name атрибута класса

View - базовый класс для обработчиков Django

get_formset - здесь для того, чтобы избежать дублирование кода
принимает аргумент data, и вызывает ModuleFormSet опреленный нами в forms.py
аргумент instance в формсете ModuleFormSet нужен для определения родительской модели 
(parent_model в inlineformset_factory) аргумент data - для изменения дочерних моделей
ссылающихся на главную многие к одному.

dispatch
метода, который определен в базовом классе View.
Принимает объект запроса (request) и его параметры
и пытается вызвать метод в python коде непосредственно в классе View
(и в классах, которые от него заимствуются), который соответствует методу HTTP запроса
Если запрос отправлен с методом GET то вызовет метод get() в класса
Если POST - то post()

Логика такая:
if request.method.lower() in self.http_method_names:
    handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
else:
    handler = self.http_method_not_allowed

Важно помнить, то в методе python (от класса View) методы get и post
вызываются после метода dispatch(отправить) и параметры request (динамически изменяющиеся параметры url)
будут передаваться в get и post те же самые, что передавались и в dispatch
т.е. в get и post передаются эти параметры от dispatch.
Поэтому при заимствовании логики работы dispatch от базового View - 
super().dispatch(some_arguments) важно положить туда нужные аргументы,
какие нужны для get и post запроса. Я уже по жесткому ошибся с этим методом,
передав при super туда None. Ошибок не было, но код вел себя не правильно.
"""
