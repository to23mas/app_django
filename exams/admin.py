from django.contrib import admin
from django.forms import TextInput, Textarea
from django.db import models
from .models import Exam, Question, ExamResult ,Answer, UserExamProgres, OpenRightAnswer
# Register your models here.

class SizeAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '100'})},
        models.TextField: {'widget': Textarea(attrs={'rows': 20, 'cols': 75})},
    }

admin.site.register(Exam, SizeAdmin)
admin.site.register(Question, SizeAdmin)
admin.site.register(UserExamProgres, SizeAdmin)
admin.site.register(Answer)
admin.site.register(OpenRightAnswer, SizeAdmin)
admin.site.register(ExamResult)
