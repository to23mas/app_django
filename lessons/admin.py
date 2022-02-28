from django.contrib import admin

from .models import Lesson, Requirements, Goals, Chapter, Content

admin.site.register(Lesson)
admin.site.register(Requirements)
admin.site.register(Goals)
admin.site.register(Chapter)
admin.site.register(Content)
# Register your models here.
