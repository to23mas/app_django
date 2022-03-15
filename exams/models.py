from django.db import models
from django.contrib.auth.models import User


class Exam(models.Model):
    exam_header = models.CharField(max_length=200)
    exam_intro = models.TextField(max_length=1000)
    exam_time = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return str(self.id) + ' - ' + self.exam_header


class Question(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    question_text = models.TextField(max_length=200)
    tags = (
        ("MULTI", 'multi'),
        ("SINGLE", "single"),
        ("OPEN", "open")
    )
    type_tag = models.CharField(max_length=10, default="SINGLE", choices=tags)

    def __str__(self):
        return self.question_text


class Answer(models.Model):
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE)
    exam_id = models.ForeignKey(Exam, on_delete=models.CASCADE, blank=True, null=True)
    answer_text = models.TextField(max_length=1000)
    tags = (
        ("RIGHT", 'right'),
        ("WRONG", "wrong")
    )
    answer_tag = models.CharField(max_length=10, default="WRONG", choices=tags)

    def __str__(self):
        return self.question_id.__str__() + ' - ' + self.answer_text


class UserExamProgres(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    completed = models.IntegerField(blank=True, null=True, default=0)
    aviable = models.IntegerField(blank=True, null=True, default=0)

    def __str__(self):
        return self.user.username


class OpenRightAnswer(models.Model):
    question = models.OneToOneField(
        Question,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    exam_id = models.ForeignKey(Exam, on_delete=models.CASCADE, blank=True, null=True)

    right_answer = models.TextField(max_length=200)

    def __str__(self):
        return self.question.question_text + ' - ' + self.right_answer


class ExamResult(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    user_id = models.IntegerField(blank=True, null=True, default=0)
    correct = models.IntegerField(blank=True, null=True, default=0)
    wrong = models.IntegerField(blank=True, null=True, default=0)
    percentage = models.IntegerField(blank=True, null=True, default=0)
    take = models.IntegerField(blank=True, null=True, default=1)
    lock = models.TimeField(blank=True, null=True)

    def __str__(self):
        return self.exam.exam_header
