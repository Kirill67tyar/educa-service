from django.db import models
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

from courses.fields import OrderField
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
    order = OrderField(
        blank=True,
        for_fields=['course', ],
        verbose_name='Номер модуля'
    )

    def __str__(self):
        return f'{self.order}. {self.title}'

    class Meta:
        ordering = ('order',)
        verbose_name = 'Модуль'
        verbose_name_plural = 'Модули'


# мы здесь сделали обощённую связь, чтобы соединить объекты типа Content
# с любой другой моделью, представляющей тип содержимого
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
        limit_choices_to={
            # ограничиваем модели, к которым может быть привязан content_type
            # (это ограничение скорее всего на уровне django, не db)
            'model__in': (
                'text', 'image', 'file', 'video',
            )
        }
    )
    object_id = models.PositiveIntegerField(  # Идентификатор связанного объекта (будет в бд)
        verbose_name='ID объекта'
    )
    item = GenericForeignKey(  # обощает данные предыдущих двух полей (не будет в бд)
        ct_field='content_type',
        fk_field='object_id'
    )
    order = OrderField(
        blank=True,
        for_fields=['module', ],
        verbose_name='Номер задания'
    )

    def __str__(self):
        return f'{self.order}. {self.content_type.name}'

    class Meta:
        ordering = ('order',)
        verbose_name = 'Контент'
        verbose_name_plural = 'Контенты'


class BaseItem(models.Model):
    owner = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='%(class)s_created',
        # django сам создаст related_name для каждой из моделей (file_created, text_created, и т.д.)
        verbose_name='Автор вопроса'
    )
    title = models.CharField(
        max_length=250,
        verbose_name='Вопрос'
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Создан'
    )
    updated = models.DateTimeField(
        auto_now=True,
        verbose_name='Обновлён'
    )

    class Meta:
        abstract = True


class Text(BaseItem):
    content = models.TextField(
        verbose_name='Текст вопроса'
    )


class Image(BaseItem):
    file = models.FileField(
        upload_to='images',
        verbose_name='относительный URL картинки'
    )


class File(BaseItem):
    file = models.FileField(
        upload_to='files',
        verbose_name='относительный URL файла'
    )


class Video(BaseItem):
    url = models.URLField(verbose_name='абсолютный URL видео')
