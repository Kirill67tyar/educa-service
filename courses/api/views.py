from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BasicAuthentication
from rest_framework.generics import (ListAPIView, RetrieveAPIView, get_object_or_404, )

from courses.models import Subject, Course
from courses.api.serializers import (
    SubjectSerializer,
    CourseSerializer
)


class SubjectListAPIView(ListAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer


class SubjectDetailAPIView(RetrieveAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer


class CourseListAPIView(ListAPIView):
    queryset = Course.objects.all().prefetch_related('modules')
    serializer_class = CourseSerializer


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
