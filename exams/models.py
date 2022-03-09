from django.db import models
from django.contrib.auth.models import User


class Exam(models.Model):
    exam_header = models.CharField(max_length=200)
    exam_intro = models.TextField(max_length=1000)
    exam_time = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return str(self.id) + ' - ' + self.exam_header


class Question(models.Model):
    exam_sets = models.ForeignKey(Exam, on_delete=models.CASCADE)
    exam_task = models.TextField(max_length=200)
    tags = (
        ("MULTI", 'multi'),
        ("SINGLE", "single"),
        ("OPEN", "open")
    )
    type_tag = models.CharField(max_length=10, default="SINGLE", choices=tags)

    def __str__(self):
        return self.exam_task


class Answer(models.Model):
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE)
    question_text = models.TextField(max_length=1000)
    tags = (
        ("RIGHT", 'right'),
        ("WRONG", "wrong")
    )
    question_tag = models.CharField(max_length=10, default="WRONG", choices=tags)

    def __str__(self):
        return self.question_id.__str__() + ' - ' + self.question_text


class UserExamProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    completed = models.IntegerField(blank=True, null=True, default=0)
    aviable = models.IntegerField(blank=True, null=True, default=0)

    def __str__(self):
        return self.user.username
