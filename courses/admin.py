from django.contrib import admin
from courses.models import (
    Subject, Course, Module, Content,
)


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug',)
    prepopulated_fields = {
        'slug': ('title',)
    }


class ModuleInline(admin.StackedInline):
    model = Module


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'subject', 'owner', 'created',)
    list_filter = ('subject', 'created',)
    search_fields = ('title', 'description',)
    inlines = (ModuleInline,)
    prepopulated_fields = {
        'slug': ('title',)
    }


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = 'pk', 'module', 'order',
