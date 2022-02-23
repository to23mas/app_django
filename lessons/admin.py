from django.contrib import admin

from .models import Lesson, Requirements, Goals, Chapter

admin.site.register(Lesson)
admin.site.register(Requirements)
admin.site.register(Goals)
admin.site.register(Chapter)
# Register your models here.
