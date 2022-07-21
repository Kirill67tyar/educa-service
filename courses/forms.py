from django.forms import inlineformset_factory

from courses.models import Course, Module

# набор форм, когда объекты одной модели (Module)
# будут связаны с объектами другой модели (Course)
ModuleFormSet = inlineformset_factory(  # фабричная функция https://habr.com/ru/post/451324/
    parent_model=Course,
    model=Module,
    fields=['title', 'description', ],  # поля, которые будут направлены для каждой формы набора
    extra=2,  # кол-во дополнительных пустых форм модулей
    can_delete=True  # добавляет для каждой формы чекбокс с помощью котого можно отметить объект у кдалению
)
# inlineformset_factory специально для подчиненных моделей, которые связаны с
# главной моделью многие к одному.
