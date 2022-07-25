from django.urls import path

from courses.views import (
    ManageCourseListView,
    CourseCreateView,
    CourseUpdateView,
    CourseDeleteView,
    CourseModuleUpdateView,
    ContentCreateUpdateView,
    ContentDeleteView,
    ModuleContentListView,
    ModuleOrderView,
    ContentOrderView,
    CourseListView,
    CourseDetailView,
)

app_name = 'courses'

urlpatterns = [
    # работа с курсами
    path('list/', ManageCourseListView.as_view(), name='manage_course_list'),  # список курсов пользователя
    path('create/', CourseCreateView.as_view(), name='course_create'),  # создание нового курса
    path('<int:pk>/update/', CourseUpdateView.as_view(), name='course_update'),  # изменение курса
    path('<int:pk>/delete/', CourseDeleteView.as_view(), name='course_delete'),  # удаление курса

    # список | добавление | изменение | удаление модулей
    path('<int:pk>/module/', CourseModuleUpdateView.as_view(), name='module_update'),

    # content create | update | delete
    path('module/<int:module_id>/content/<str:model_name>/create/', ContentCreateUpdateView.as_view(),
         name='content_create'),  # создать контент
    path('module/<int:module_id>/content/<str:model_name>/update/<int:pk>/', ContentCreateUpdateView.as_view(),
         name='content_update'),  # изменить контент
    path('content/<int:content_id>/delete/', ContentDeleteView.as_view(), name='content_delete'),  # удалить контент
    # список контента в модуле
    path('module/<int:module_id>/list/', ModuleContentListView.as_view(), name='module_content_list'),

    # change order (взаимодействуют с обработчиками js и изменяют order у Module и Content)
    path('module/order/', ModuleOrderView.as_view(), name='module_order_change'),
    path('content/order/', ContentOrderView.as_view(), name='content_order_change'),

    # просмотр курсов для учащихся
    path('subject/<slug:subject_slug>/', CourseListView.as_view(), name='course_list_subject'),  # список по предмету
    path('', CourseListView.as_view(), name='course_list'),  # список
    path('<slug:slug>/', CourseDetailView.as_view(), name='course_detail'),  # список
]
