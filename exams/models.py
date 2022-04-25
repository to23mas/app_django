"""
Models

model pro aplikaci exams

classes: Examl, Question, Answer, OpenRightAnswer, ExamResult,
        AviableTest, CompleteTest, FailedTest

@author: Tomáš Míčka

@contact: to23mas@gmail.com

@version:  1.0
"""

from django.db import models
from django.contrib.auth.models import User


class Exam(models.Model):
    """Třída představující jednotlivé Testy

        @param exam_header: nadpis testu
        @param exam_intro: úvodní popis testu
        @param exam_time: předpokládaný čas na napsání
        @param exam_number: pořadí testu .. odpovídá ID

    """
    exam_header = models.CharField(max_length=200)  # nadpis testu
    exam_intro = models.TextField(max_length=1000)  # úvod popis
    exam_time = models.IntegerField(blank=True, null=True)  # předpokládaná délka testu ..
    exam_number = models.IntegerField(blank=True, null=True)
    def __str__(self):
        """funkce pro výpis -> ID - NADPIS"""
        return str(self.id) + ' - ' + self.exam_header  # 1 - ÚVODNÍ TEST


class Question(models.Model):
    """Třída představující jednotlivé otázky k testům.

        @param exam: cizí klíč testu
        @param question_text: vlastní text otázky
        @param q_html: text s vyescapovanými html elementy
        @param type_tag: druh otázky

    """

    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)  # každá otázka má jeden test
    question_text = models.TextField(max_length=2000) # vlastní text otázky
    q_html = models.TextField(max_length=2000, blank=True, null=True, default='')
    tags = (
        ("MULTI", 'multi'),
        ("SINGLE", "single"),
        ("OPEN", "open")
    )
    type_tag = models.CharField(max_length=10, default="SINGLE", choices=tags)  # tři druhy otázek

    def __str__(self):
        """funkce pro výpis -> ID - OTÁZKA"""
        return f"{self.exam.id} - {self.question_text}"


class Answer(models.Model):
    """Třída představující odpovědi na otázky.

        @param question_id: cizí klíč otázky
        @param exam_id: cizí klíč testu
        @param answer_text: vlastní text odpovědi
        @param answer_tag: jestli je správná nebo ne

    """
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE)  # odpověď patří k otázce
    exam_id = models.ForeignKey(Exam, on_delete=models.CASCADE, blank=True, null=True)  # zároveň patří k testu
    answer_text = models.TextField(max_length=1000)  # text odpověďi
    tags = (
        ("RIGHT", 'right'),
        ("WRONG", "wrong")
    )
    answer_tag = models.CharField(max_length=10, default="WRONG", choices=tags)  # jedná se o správnou nebo ne

    def __str__(self):
        """funkce pro výpis -> ID - ODPOVĚD"""
        return self.question_id.__str__() + ' - ' + self.answer_text





class OpenRightAnswer(models.Model):
    """Třída představující odpovědi na otevřené otázky.

        @param question: One To One na Otázku
        @param exam_id: cizí klíč testu
        @param right_answer: co je správná odpověď
    """
    question = models.OneToOneField(
        Question,
        on_delete=models.CASCADE,
        primary_key=True,
    )  # 1:1 k otázce
    exam_id = models.ForeignKey(Exam, on_delete=models.CASCADE, blank=True, null=True)  # testu

    right_answer = models.TextField(max_length=200)  # správná odpověď

    def __str__(self):
        """funkce pro výpis -> TEXT_OTÁZKY - TEXT_ODPOVĚDI"""
        return self.question.question_text + ' - ' + self.right_answer


class ExamResult(models.Model):
    """Třída představující výsledky napsaného testu.

        @param exam: cizí klíč testu
        @param user_id: ID uživalte
        @param correct: počet správných odpovědí
        @param wrong: počet špatných odpovědí
        @param percentage: poměř správných ke špatným
        @param take: o kolikátý pokus o napsání testu se jedná
        @param lock: kdy došlo k zamčení testu
        @param lock_date: jakého dne došlo k zamčení

    """
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    user_id = models.IntegerField(blank=True, null=True, default=0)
    correct = models.IntegerField(blank=True, null=True, default=0)
    wrong = models.IntegerField(blank=True, null=True, default=0)
    percentage = models.IntegerField(blank=True, null=True, default=0)
    take = models.IntegerField(blank=True, null=True, default=1)
    lock = models.TimeField(blank=True, null=True)
    lock_date = models.DateField(blank=True, null=True)

    def __str__(self):
        """funkce pro výpis -> USERNAME - ID_UŽIVATELE - NADPIS TESTU"""
        return f"{self.get_username()}({self.user_id}) {self.exam.exam_header}"

    def get_username(self):
        """funkce vrátí uživatelovo jméno"""
        return User.objects.get(id=self.user_id)


class AviableTest(models.Model):
    """Třída představující Test který ještě uživatel nezkusil

        @param user: cizí klíč uživatele
        @param aviable_exam: cizí klíč testu
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # uživatel
    aviable_exam = models.ForeignKey(Exam, on_delete=models.CASCADE)

    def __str__(self):
        """funkce pro výpis -> USERNAME - ID_UŽIVATELE - NADPIS TESTU"""
        return f"{self.user.username} - {self.aviable_exam.exam_header}"


class CompleteTest(models.Model):
    """Třída představující Test který je úspěšně splněný

    @param user: cizí klíč uživatele
    @param complete_exam: cizí klíč testu
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # uživatel
    complete_exam = models.ForeignKey(Exam, on_delete=models.CASCADE)

    def __str__(self):
        """funkce pro výpis -> USERNAME - ID_UŽIVATELE - NADPIS TESTU"""
        return self.user.username

class FailedTest(models.Model):
    """Třída představující Test, jehož výsledek nepřesáhl potřebný počet bodů pro splnění

        @param user: cizí klíč uživatele
        @param complete_exam: cizí klíč testu
        @param take: celkový počet pokusů
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # uživatel
    failed_exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    take = models.IntegerField(blank=True, null=True, default=1)
    def __str__(self):
        """funkce pro výpis -> USERNAME - ID_UŽIVATELE - NADPIS TESTU"""
        return f"{self.user.username} - {self.failed_exam.exam_header}"
