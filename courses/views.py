from django.apps import apps
from django.urls import reverse_lazy
from django.forms import modelform_factory
from django.views.generic.base import TemplateResponseMixin
from django.shortcuts import (
    redirect, render, get_object_or_404,
)
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
)
from django.views.generic import (
    View, ListView, CreateView,
    UpdateView, DetailView, DeleteView,
)

from courses.forms import ModuleFormSet
from courses.models import (
    Subject, Course,
    Module, Content,
    Text, File, Image, Video,
)
from common.analize.analizetools import (
    p_dir, p_mro, p_glob, p_loc, p_type,
    delimiter, p_content, show_builtins,
    show_doc, console, console_compose,
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

    def get_queryset(self):
        return super().get_queryset().prefetch_related('modules')


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
            от того какой метод у HTTP запроса
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


# LoginRequiredMixin
class ContentCreateUpdateView(TemplateResponseMixin, View):
    obj = None
    model = None
    module = None
    template_name = 'courses/manage/content/form.html'

    @staticmethod
    def get_model(model_name):
        # так
        if model_name in ('text', 'file', 'image', 'video',):
            return apps.get_model(
                app_label='courses',  # название приложения где находится модель
                model_name=model_name,  # имя модели передаваемое через URL (в нижнем регистре)
                require_ready=True
            )
        # # или так
        # models_dict = {
        #     'text': Text,
        #     'file': File,
        #     'image': Image,
        #     'video': Video,
        # }
        # return models_dict.get(model_name)

    def get_form(self, data=None, files=None):
        form = modelform_factory(
            model=self.model,
            exclude=(
                'owner',
                'created',
                'updated',
            )
        )
        return form(instance=self.obj, data=data, files=files)

    def dispatch(self, request, module_id,
                 model_name, pk=None, *args, **kwargs):
        """
            здесь мы находим модель (text|file|image|video)
            и какой конкретно модуль
            а также если есть pk то с каким конкретно экземпляром контента мы работаем
            дальше dispatch вызывает метод в класса, который соответствует таковому в HTTP запросе
        """
        self.model = self.get_model(model_name=model_name)
        self.module = get_object_or_404(
            klass=Module,
            pk=module_id,
            course__owner=request.user

        )
        if pk:
            self.obj = get_object_or_404(
                klass=self.model,
                pk=pk,
                owner=request.user
            )
        return super(ContentCreateUpdateView, self).dispatch(request, pk, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.get_form()
        return self.render_to_response(
            context={
                'form': form,
                'object': self.obj,
                'module': self.module,
            }
        )

    def post(self, request, pk, *args, **kwargs):
        form = self.get_form(
            data=request.POST,
            files=request.FILES
        )
        if form.is_valid():
            item = form.save(commit=False)
            item.owner = request.user
            item.save()
            if not pk:
                Content.objects.create(
                    module=self.module,
                    item=item
                )
            return redirect(reverse_lazy('courses:module_content_list',
                                         kwargs={
                                             'module_id': self.module.pk,
                                         }))
        return self.render_to_response(
            context={
                'form': form,
                'object': self.obj,
                'module': self.module,
            }
        )


class ContentDeleteView(View):
    def post(self, request, content_id, *args, **kwargs):
        content = get_object_or_404(
            klass=Content,
            pk=content_id,
            module__course__owner=request.user
        )
        module = content.module
        content.item.delete()
        content.delete()
        return redirect(reverse_lazy('courses:module_content_list',
                                     kwargs={
                                         'module_id': module.pk,
                                     }))


class ModuleContentListView(TemplateResponseMixin, View):
    template_name = 'courses/manage/module/list.html'

    def get(self, request, module_id, *args, **kwargs):
        module = get_object_or_404(
            klass=Module,
            pk=module_id,
            course__owner=request.user
        )
        return self.render_to_response(
            context={'module': module, }
        )


"""

шаблоны урлов для этого обработчика используется следующие:
'module/<int:module_id/content/<str:model_name>/create/ - для create
'module/<int:module_id/content/<str:model_name>/<int:pk>/ - для update

где: 
module_id - id одного из модулей
model_name - имя одной из потенциальных моделей привязанных к Content 
(тройной связью при помощи ContentType) ['text', 'file', 'image', 'video',]
pk - id этого типа контента, если мы используем update

ContentCreateUpdateView 
Заимствован от TemplateResponseMixin View
get_model model_name *args, **kwargs
model_name должен быть именем одной из модели - ['text', 'file', 'image', 'video',]
get_form model, *args, **kwargs
используем modelform_factory которая создаст модельную форму сама, исключив поля
указанные в именованном аргументе exclude
dispatch

перед тем, как dispatch решит какой метод у этого http запроса, и какой метод
соответственно надо вызывать в классе заимствованном от View - get или post
1) мы молжны определеть  каким модулем мы работаем конкретно
2) какая у нас модель типа данных для Content - text, file, image, video
3) если в url передался pk для действия update то должны узнать, не только модель
типа данных для Content но и с какой конкретно записью из таблицы мы работаем
get

при get передаем в контекст форму, куда кладем именованный аргумент instance=self.obj
если self.obj будет None, то будет пустая форма,
а если у нас действие update то передаст экземпляр нужной модели
post
кладем в форму request.POST и request.FILES. 
если валидная, то присаиваем нужного овнера
если pk в url не передавалась, то отработал шаблон с /create/
значит нужно создать новую запись в таблице courses_content
с помощью ORM Django и модели Content. Но связь там не обычная,
а обощенная, привязанная к модели ContentType
Это мне меньше всего понятно, ведь создание связи с ContentType не такое-же
как с другой моделью.
"""

"""
Примиси (Mixins) - это класс, который используется при множественном наследовании.
При определении класса можно задействовать несколько примесей, каждая из которых добавит
часть функций в класс.

Примеси удобны в двух случаях:
1 - нужно использовать несколько различных функций в рамках моего класса
2 - реализовать одну и туже функциональность в нескольких классах
В rest_framework тоже используются миксины для CRUD функционала
Вспомни, миксины в rest_framework добавляют нам функционал list, retrieve,create, update, partial_update, destroy
И работают они совместно с GenericApiView
Чтобы определять самому миксины - нужно хорошо разбираться в django, какие методы, за что отвечают,
какие вызываются и когда, какие атрибуты используются.

*****Разбор классов обработчиков, и логики кастомных миксинов*****

OwnerMixin
базовый миксин для работы owner.

OwnerEditMixin - для CreateView и UpdateView (переопределяем form_valid), для работы с owner

OwnerCourseMixin 
унаследован от - OwnerMixin, LoginRequiredMixin
класс для работы с курсом. будет использоваться для функционала Read и Delete

OwnerCourseEditMixin 
унаследован от - OwnerCourseMixin OwnerEditMixin
допалняет необходимую инфу (атрибуты) для CreateView и UpdateView
класс для работы с курсом. будет использоваться для функционала Create и Update

ManageCourseListView 
унаследован от - OwnerCourseMixin ListView
Для функционала Read

CourseCreateView 
унаследован от - PermissionRequiredMixin OwnerCourseEditMixin CreateView
Для функционала Create

CourseUpdateView OwnerCourseEditMixin UpdateView
унаследован от - PermissionRequiredMixin OwnerCourseEditMixin UpdateView
Для функционала Update

CourseDeleteView OwnerCourseMixin DeleteView
унаследован от - PermissionRequiredMixin OwnerCourseMixin DeleteView
Для функционала Delete
Атрибуты и методы этих классов:
form_valid(self, form) - определена в ModelFormMixin (from django.views.generic.edit import ModelFormMixin)
или чуть раньше. Не путать с методом is_valid форм.
работает с формами и модельными формами - CreateView, UpdateView. Метод выполняется, когда форма
успешно проходит валидацию.

Поведение по умоланию:
-- сохранение объекта в бд (для модельных форм)
-- перенаправление пользователя на страницу по адресу success_url (для обыных форм)
Пока не до конца понятно как он работает, но он как-то связан с CreateView, UpdateView
про form_valid есть здесь https://docs.djangoproject.com/en/3.2/ref/class-based-views/generic-editing/
Помни, что для CreateView и UpdateView в шаблоне будет доступна переменная из контекта - form
больше всего меня обескуражила строчка form.instance.owner = self.request.user в form_valid(form)
как минимум у обычных форм нету instance как до так и после валидации (во всяком случае у невалидных)
fields (в OwnerCourseEditMixin) поля модели, из которых будет формироваться объект обрабочиками
CreateView и UpdateView. Возможно - по большей части для ModelForm от CreateView и UpdateView
success_url - тоже для CreateView и UpdateView - куда перенаправлять в случае успешной обработки
формы классами CreateView и UpdateView
!!! Оень важный момент - в базовом View url параметры доступны в self.kwargs. 
Не путать self.kwargs с kwargs который мы передаем в функцию.
"""
