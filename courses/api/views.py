from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.authentication import BasicAuthentication
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    get_object_or_404,
)

from courses.models import Subject, Course
from courses.api.permissions import IsEnrolledPermission
from courses.api.serializers import (
    SubjectSerializer,
    CourseSerializer,
    CourseWithContentSerializer,

)


class SubjectListAPIView(ListAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer


class SubjectDetailAPIView(RetrieveAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer


class CourseViewSet(ReadOnlyModelViewSet):
    # доступны методы list, и retrieve (GET запрос)
    queryset = Course.objects.all().prefetch_related('modules__contents')
    serializer_class = CourseSerializer

    @action(  # https://www.django-rest-framework.org/community/3.8-announcement/#deprecations
        methods=['post', ],
        detail=True,  # это значит что роутер будет обрабатывать это когда один экземпляр, иначе detail=False
        url_path='new-path-enroll',
        authentication_classes=[BasicAuthentication, ],
        permission_classes=[IsAuthenticated, ]
    )
    def enroll(self, request, *args, **kwargs):
        """
        скорее всего по названию метода enroll
        и формируется url для этого обработчика
        хотя, если в декоратора action
        способ поменять url - url_path='new-path-enroll'
        """
        course = self.get_object()  # как и get_queryset доступен от GenericAPIView
        user = request.user
        if user in course.students.all():
            return Response({'already enrolled': True, })
        else:
            course.students.add(user)
            return Response({'enrolled': True, })

    @action(
        methods=['get', ],
        detail=True,
        url_path='contents',
        serializer_class=CourseWithContentSerializer,
        authentication_classes=[BasicAuthentication, ],
        permission_classes=[IsEnrolledPermission, ]  # BasicAuthentication
    )
    def courses(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


# можно сделатьь это в виде обработчика
# а можно реализовать это в viewsets,
# как и сделано выше
class CourseEnrollAPIView(APIView):
    http_method_names = ['post', ]
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, pk, format=None):
        user = request.user
        course = get_object_or_404(Course, pk=pk)
        if user not in course.students.all():
            course.students.add(user)
            return Response({'enrolled': True, })
        else:
            return Response({'already enrolled': True, })
