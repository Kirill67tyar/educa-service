from rest_framework import routers

from django.urls import path, include

from courses.api.views import (
    SubjectDetailAPIView,
    SubjectListAPIView,
    CourseViewSet,
    CourseEnrollAPIView,
)

app_name = 'api'

# не совсем понятно как это работает
# https://www.django-rest-framework.org/api-guide/routers/#routers
router = routers.DefaultRouter()
router.register(
    prefix='courses',  # скорее всего то, по какому url это будет доступно
    viewset=CourseViewSet
    # наш viewset, который мы определили (в данном случае заимствованный от ReadOnlyModelViewSet)
)

urlpatterns = [
    path('subjects/', SubjectListAPIView.as_view(), name='list_subject'),
    path('subjects/<int:pk>/', SubjectDetailAPIView.as_view(), name='detail_subject'),
    # path('courses/<int:pk>/enroll/', CourseEnrollAPIView.as_view(), name='courses-enroll'),
    path('', include(router.urls)),  # и здесь мы подключаем на router
]
