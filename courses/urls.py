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
)

app_name = 'courses'

urlpatterns = [
    path('list/', ManageCourseListView.as_view(), name='manage_course_list'),
    path('create/', CourseCreateView.as_view(), name='course_create'),
    path('<int:pk>/update/', CourseUpdateView.as_view(), name='course_update'),
    path('<int:pk>/delete/', CourseDeleteView.as_view(), name='course_delete'),
    path('<int:pk>/module/', CourseModuleUpdateView.as_view(), name='module_update'),

    # content create | update | delete
    path('module/<int:module_id>/content/<str:model_name>/create/', ContentCreateUpdateView.as_view(),
         name='content_create'),
    path('module/<int:module_id>/content/<str:model_name>/update/<int:pk>/', ContentCreateUpdateView.as_view(),
         name='content_update'),
    path('content/<int:content_id>/delete/', ContentDeleteView.as_view(), name='content_delete'),
    path('module/<int:module_id>/list/', ModuleContentListView.as_view(), name='module_content_list'),
]
