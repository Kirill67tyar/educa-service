from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, CreateView,
    UpdateView, DetailView, DeleteView,
)

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
        super().form_valid(form)


class OwnerCourseMixin(OwnerMixin):
    model = Course

    # можно убрать наследование от OwnerMixin, потому что он дальше
    # нигде не используется
    # def get_queryset(self):
    #     qs = super().get_queryset()
    #     return qs.filter(owner=self.request.user)
    #     # return self.model.objects.filter(owner=self.request.user)


class OwnerCourseEditMixin(OwnerCourseMixin, OwnerEditMixin):
    fields = [
        'subject', 'title', 'slug', 'description',
    ]
    success_url = reverse_lazy('courses:manage_course_list')
    template_name = 'courses/form.html'


class ManageCourseListView(OwnerCourseMixin, ListView):
    template_name = 'courses/list.html'


class CourseCreateView(OwnerCourseEditMixin, CreateView):
    pass


class CourseUpdateView(OwnerCourseEditMixin, UpdateView):
    pass


class CourseDeleteView(OwnerCourseMixin, DeleteView):
    template_name = 'courses/delete.html'
    success_url = reverse_lazy('courses:manage_course_list')
