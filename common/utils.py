
from django.db.models.query import QuerySet
from django.db.models.manager import BaseManager


def get_object_or_null(model, **kwargs):
    if isinstance(model, QuerySet) or isinstance(model, BaseManager):
        return model.filter(**kwargs).first()
    return model.objects.filter(**kwargs).first()



"""fixtures/subjects_courses_modules.json"""