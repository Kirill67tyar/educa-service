from rest_framework.relations import HyperlinkedIdentityField
from rest_framework.serializers import ModelSerializer

from courses.models import (
    Subject, Course, Module,
)


class SubjectSerializer(ModelSerializer):
    class Meta:
        model = Subject
        fields = [  # если не указывать fields, то по умолчанию будут добавляться все поля
            'id', 'title', 'slug',
        ]


class ModuleSerializer(ModelSerializer):
    class Meta:
        model = Module
        fields = [
            'title',
            'description',
            'order',
        ]


class CourseSerializer(ModelSerializer):
    modules = ModuleSerializer(many=True, read_only=True)
    # url_to_enroll = HyperlinkedIdentityField(
    #     view_name='api:courses-enroll'
    # )  # т.к. запись доступна по Post запросу, то это поле не годится

    class Meta:
        model = Course
        fields = [
            'id',
            'title',
            'slug',
            'description',
            'created',
            'owner',
            'subject',
            'modules',
            # 'url_to_enroll',
        ]
