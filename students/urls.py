from django.urls import path
from django.views.decorators.cache import cache_page

from students.views import (
    StudentRegistrationView,
    StudentEnrollCourseView,
    StudentCourseListView,
    StudentCourseDetailView,
    empty_view
)

app_name = 'students'

urlpatterns = [
    path('register/', StudentRegistrationView.as_view(), name='register'),
    path('enroll-course/', StudentEnrollCourseView.as_view(), name='student_enroll_course'),
    path('empty/', empty_view, name='empty'),
    path('courses/', cache_page(60 * 10)(StudentCourseListView.as_view()), name='student_course_list'),
    path('course/<slug:slug>/', cache_page(60 * 10)(StudentCourseDetailView.as_view()), name='student_course_detail'),
    path('course/<slug:slug>/<int:module_id>/', cache_page(60 * 10)(StudentCourseDetailView.as_view()), name='student_course_detail_module'),
]
