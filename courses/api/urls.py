from django.urls import path
from courses.api.views import (
    SubjectDetailAPIView,
    SubjectListAPIView,
    CourseListAPIView,
    CourseEnrollAPIView,
)

app_name = 'api'

urlpatterns = [
    path('subjects/', SubjectListAPIView.as_view(), name='list_subject'),
    path('subjects/<int:pk>/', SubjectDetailAPIView.as_view(), name='detail_subject'),
    path('courses/', CourseListAPIView.as_view(), name='courses_list'),
    path('courses/<int:pk>/enroll/', CourseEnrollAPIView.as_view(), name='courses-enroll'),
]
