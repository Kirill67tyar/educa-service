from django.urls import path
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
    path('courses/', StudentCourseListView.as_view(), name='student_course_list'),
    path('course/<slug:slug>/', StudentCourseDetailView.as_view(), name='student_course_detail'),
    path('course/<slug:slug>/<int:module_id>/', StudentCourseDetailView.as_view(), name='student_course_detail_module'),
]
