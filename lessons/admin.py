from django.contrib import admin

from .models import Lesson, Requirements, Goals, Chapter, Content, Progress

admin.site.register(Lesson)
admin.site.register(Requirements)
admin.site.register(Goals)
admin.site.register(Chapter)
admin.site.register(Content)
admin.site.register(Progress)
# Register your models here.
