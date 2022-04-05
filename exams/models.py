from django.db import models
from django.contrib.auth.models import User


class Exam(models.Model):
    """ Exam představuje model pro jednotlivé tety exam s id == 1 => test číslo jedna"""
    exam_header = models.CharField(max_length=200)  # nadpis testu
    exam_intro = models.TextField(max_length=1000)  # úvod popis
    exam_time = models.IntegerField(blank=True, null=True)  # předpokládaná délka testu .. TODO neimplementováno
    exam_number = models.IntegerField(blank=True, null=True)
    def __str__(self):
        return str(self.id) + ' - ' + self.exam_header  # 1 - ÚVODNÍ TEST


class Question(models.Model):
    """model pro otázky"""
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)  # každá otázka má jeden test
    question_text = models.TextField(max_length=200)  # vlastní text otázky
    tags = (
        ("MULTI", 'multi'),
        ("SINGLE", "single"),
        ("OPEN", "open")
    )
    type_tag = models.CharField(max_length=10, default="SINGLE", choices=tags)  # tři druhy otázek

    def __str__(self):
        return f"{self.exam.id} - {self.question_text}"


class Answer(models.Model):
    """odpovědi k otázkám"""
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE)  # odpověď patří k otázce
    exam_id = models.ForeignKey(Exam, on_delete=models.CASCADE, blank=True, null=True)  # zároveň patří k testu
    answer_text = models.TextField(max_length=1000)  # text odpověďi
    tags = (
        ("RIGHT", 'right'),
        ("WRONG", "wrong")
    )
    answer_tag = models.CharField(max_length=10, default="WRONG", choices=tags)  # jedná se o správnou nebo ne

    def __str__(self):
        return self.question_id.__str__() + ' - ' + self.answer_text





class OpenRightAnswer(models.Model):
    """správná odpověď k otázce"""
    question = models.OneToOneField(
        Question,
        on_delete=models.CASCADE,
        primary_key=True,
    )  # 1:1 k otázce
    exam_id = models.ForeignKey(Exam, on_delete=models.CASCADE, blank=True, null=True)  # testu

    right_answer = models.TextField(max_length=200)  # správná odpověď

    def __str__(self):
        return self.question.question_text + ' - ' + self.right_answer


class ExamResult(models.Model):
    """Výsledek jednotlivých tstů"""
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    user_id = models.IntegerField(blank=True, null=True, default=0)
    correct = models.IntegerField(blank=True, null=True, default=0)
    wrong = models.IntegerField(blank=True, null=True, default=0)
    percentage = models.IntegerField(blank=True, null=True, default=0)
    take = models.IntegerField(blank=True, null=True, default=1)
    lock = models.TimeField(blank=True, null=True)
    lock_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.get_username()}({self.user_id}) {self.exam.exam_header}"

    def get_username(self):
        return User.objects.get(id=self.user_id)


class AviableTest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # uživatel
    aviable_exam = models.ForeignKey(Exam, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.aviable_exam.exam_header}"


class CompleteTest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # uživatel
    complete_exam = models.ForeignKey(Exam, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class FailedTest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # uživatel
    failed_exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    take = models.IntegerField(blank=True, null=True, default=1)
    def __str__(self):
        return f"{self.user.username} - {self.failed_exam.exam_header}"
