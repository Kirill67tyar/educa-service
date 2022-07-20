from django.db.models import PositiveIntegerField
from django.core.exceptions import ObjectDoesNotExist


class OrderField(PositiveIntegerField):
    def __init__(self, for_fields=None, *args, **kwargs):
        self.for_fields = for_fields
        super(OrderField, self).__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        """
            pre_save выполняется перед тем как django вызовет save и сделает INSERT в db
            model_instance - экземпляр модели, в котором определено поле
            self.attname - переменная за которой было закреплено поле в модели
            self.for_fields - внешнии ключи на модель по типу многие к одному
                            (для Module это ключ на Course)
            value - это значение, которое в конце будет присвоено OrderField
                    важно  pre_save именно его и возвращать
            страница 313 в django книги Антонио Меле - отлично написано
            doc:
            https://docs.djangoproject.com/en/4.0/howto/custom-model-fields/
        """
        # если пользователь не задал поле order (OrderField)
        if getattr(model_instance, self.attname) is None:
            qs = self.model.objects.all()  # достаём все объекты модели
            if self.for_fields:
                parent_model = {  # подготавливаем параметры, которые будем использовать для фильтра
                    field: getattr(model_instance, field) for field in self.for_fields
                }
                # если родительская модель, то достаём экземпляры которые привязаны только к ней
                qs = qs.filter(**parent_model)
            try:
                # если не было родительской модели, используем qs для всех объектов
                instance = qs.latest(self.attname)
                value = getattr(instance, self.attname) + 1
            except ObjectDoesNotExist:
                value = 0
            setattr(model_instance, self.attname, value)
            return value
        else:
            return super(OrderField, self).pre_save(model_instance, add)
