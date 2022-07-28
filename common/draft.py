"""
---------- Правила передачи данных в ModelSerializer
    1. нужно передавать конкретно аргументу data
    2. если мы передаём queryset, то нужно также дополнительно передать
        аргумент many=True

            SubjectSerializer(data=<some_QuerySet>, many=True)

    3. когда мы передаём в сериалайзер экземпляр модели, то аргумент many=True не нужен
    4. если мы хотим чтобы сериалайзер был только для чтения, то нужно передать аргумент read_only=True



---------- Правила сохранения в ModelSerializer
    1. такой __init__ у BaseSerializer - __init__(self, instance=None, data=empty, **kwargs)

    2. если мы хотим передать данные для сохранения, нужно передавать их аргументу data
            new_subject_serializer = SubjectSerializer(data={'id':5, 'title': 'new subject', 'slug':'new-subject',})

    3. перед тем как сохранять нужно обязательно проверить данные на валидность:
            new_subject_serializer.is_valid()
       если это не сделать будет ошибка:
            AssertionError: You must call `.is_valid()` before calling `.save()`.

    4. и после уже сохранять данные
            new_subject_serializer.save()

    5. если мы хотим посмотреть что за информация записана в конкретный сериалайзер,
        у него есть метод data
            new_subject_serializer.data  # {'id':5, 'title': 'new subject', 'slug':'new-subject',}




---------- Как DRF преврращает (парсит) JSON Объекты в Python объеты
            и обратно из Python объектов в JSON данные

из JSON превращаьб в python объекты - с помощью специального парсера - JSONParser

    у него всего 4 метода:
         'media_type',
         'parse',
         'renderer_class',
         'strict'


    Как видим JSONParser преобразовал JSON данные в байатах в python объект

        from io import BytesIO
        from rest_framework.parsers import JSONParser

        data = b'{"id":6,"title":"nature searching", "slug": "nature-searching"}' # байтовая строка
        type(data)  # <class 'bytes'>

        bytes_data = BytesIO(
            data)  # Для работы с необработанными байтами вместо текста Unicode необходимо использовать io.BytesIO.
        type(bytes_data)  # <class '_io.BytesIO'>

        json_parser_instance = JSONParser()
        py_data = json_parser_instance.parse(bytes_data)
        print(py_data)  # {'id': 6, 'title': 'nature searching', 'slug': 'nature-searching'}


из python превращаьб в JSON объекты - с помощью специального парсера - JSONParser

        from rest_framework.renderers import JSONRenderer

        JSONRenderer().render(py_data)  # b'{"id":6,"title":"nature searching","slug":"nature-searching"}'

        type(JSONRenderer().render(data=serializator.data))  # <class 'bytes'>

JSONRenderer().render преобразует объект python в байтовую строку, соответствующую формату json
и дальше эта байтовая строка отправится в теле HTTP Ответа


Итого:
    JSONParser().parse(<some_json_data_in_bytes>) # парсит из json в python
    JSONRenderer().render(some_python_dict) # рендерить из python в json

По умолчанию DRF использует два рендерера:
    JSONRenderer().render
    BrowsableAPIRenderer()

from rest_framework.renderers import BrowsableAPIRenderer
BrowsableAPIRenderer - в отличие от JSONRenderer предоставляет web-интерфейс для просмотра API
(именно благодаря BrowsableAPIRenderer мы и получаем страницу где помимо JSON данных содержится интерфейс)
можно указать рендерер по умолчанию в константе DEFAULT_RENDERER_CLASSES в настройке REST_FRAMEWORK
(именно в константе REST_FRAMEWORK и прописываются все настройки для DRF)


from rest_framework.renderers import JSONRenderer
from courses.models import Course as C
from courses.api.serializers import CourseSerializer as CS
serializator = CS(data=C.objects.all(),many=True)
serializator.data
JSONRenderer().render(data=serializator.data)
"""
from rest_framework.renderers import BrowsableAPIRenderer
