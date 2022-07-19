from django.db import models
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

from courses.utils import from_cyrilic_to_eng

User = get_user_model()


def create_slug(obj):
    if not obj.slug:
        obj.slug = slugify(from_cyrilic_to_eng(str(obj.title)))


class Subject(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name='Название'
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name='Наименование для URL'
    )

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        create_slug(self)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Предмет'
        verbose_name_plural = 'Предметы'
        ordering = ('-title',)


class Course(models.Model):
    owner = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='courses_created',
        verbose_name='Владелец курса'
    )
    subject = models.ForeignKey(
        to='Subject',
        on_delete=models.CASCADE,
        related_name='courses',
        verbose_name='Предмет'
    )
    title = models.CharField(
        max_length=200,
        verbose_name='Название'
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name='Наименование для URL'
    )
    description = models.TextField(
        verbose_name='Описание'
    )
    created = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Создан'
    )

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        create_slug(self)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'
        ordering = ('-created',)


class Module(models.Model):
    course = models.ForeignKey(
        to='Course',
        on_delete=models.CASCADE,
        related_name='modules',
        verbose_name='Курс'
    )
    title = models.CharField(
        max_length=200,
        verbose_name='Название'
    )
    description = models.TextField(
        blank=True
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Модуль'
        verbose_name_plural = 'Модули'


# мы здесь сделали обощённую связь, чтобы соединить объекты типа Content
# с любой другой моделью, педставляющей тип содержимого
class Content(models.Model):
    module = models.ForeignKey(
        to='Module',
        on_delete=models.CASCADE,
        related_name='contents',
        verbose_name='Модуль'
    )
    content_type = models.ForeignKey(  # Внешний ключ на ContentType (будет в бд)
        to=ContentType,
        on_delete=models.CASCADE,
    )
    object_id = models.PositiveIntegerField(  # Идентификатор связанного объекта (будет в бд)
        verbose_name='ID объекта'
    )
    item = GenericForeignKey(  # обощает данные предыдущих двух полей (не будет в бд)
        ct_field='content_type',
        fk_field='object_id'
    )

