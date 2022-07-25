from django.urls import path
from students.views import (
    StudentRegistrationView, empty_view
)

app_name = 'students'

urlpatterns = [
    path('register/', StudentRegistrationView.as_view(), name='register'),
    path('empty/', empty_view, name='empty'),
]
