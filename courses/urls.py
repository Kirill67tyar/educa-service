from django.urls import path

from courses.views import (
    ManageCourseListView,
)

app_name = 'courses'

urlpatterns = [
    path('list/', ManageCourseListView.as_view(), name='manage_course_list'),
]
