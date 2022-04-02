from django.contrib import admin
from django.forms import TextInput, Textarea
from django.db import models

from .models import Lesson, Requirements, Goals, Chapter, Content


class ContentAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '200'})},
        models.TextField: {'widget': Textarea(attrs={'rows': 40, 'cols': 200})},
    }


admin.site.register(Lesson)
admin.site.register(Requirements)
admin.site.register(Goals)
admin.site.register(Chapter)
admin.site.register(Content, ContentAdmin)
