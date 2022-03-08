from django.contrib import admin

from .models import Exam, Question, Answer, UserExamProgress
# Register your models here.

admin.site.register(Exam)
admin.site.register(Question)
admin.site.register(UserExamProgress)
admin.site.register(Answer)
