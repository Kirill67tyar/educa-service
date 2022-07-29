from rest_framework.serializers import ModelSerializer
from rest_framework.relations import HyperlinkedIdentityField, RelatedField

from courses.models import (
    Subject, Course, Module, Content,
)


# сериалайзер для предметов
class SubjectSerializer(ModelSerializer):
    class Meta:
        model = Subject
        fields = [  # если не указывать fields, то по умолчанию будут добавляться все поля
            'id', 'title', 'slug',
        ]


# сериалайзер для модулей (без подробного отображения контента)
class ModuleSerializer(ModelSerializer):
    class Meta:
        model = Module
        fields = [
            'title',
            'description',
            'order',
        ]


# сериалайзер для курсов (list | detail)
class CourseSerializer(ModelSerializer):
    modules = ModuleSerializer(many=True, read_only=True)

    # url_to_enroll = HyperlinkedIdentityField(
    #     view_name='api:courses-enroll'
    # )  # т.к. запись доступна только по Post запросу, то это поле не годится

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


# поле для отображения разного контента
class ItemRelatedField(RelatedField):
    def to_representation(self, value, *args, **kwargs):
        return value.render()


# сериалайзер для контента
class ContentSerializer(ModelSerializer):
    item = ItemRelatedField(read_only=True)

    class Meta:
        model = Content
        fields = ['id', 'order', 'item', ]


# серализер для модулей с подробным контентом
class ModuleWithContentSerializer(ModelSerializer):
    contents = ContentSerializer(many=True)

    class Meta:
        model = Module
        fields = [
            'title',
            'description',
            'order',
            'contents',
        ]


# сериалайзер с полем где модули с контентом отображаются по другому (подробно)
class CourseWithContentSerializer(CourseSerializer):
    modules = ModuleWithContentSerializer(many=True)
