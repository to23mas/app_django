"""
Modul s funkcionalitami zařizujícími správné zobrazení testů

classes: ExamOverview - data ohledně vypisování seznamu testů
        Test -  data jednoho testu
        ExamValidation - Validuje testy



@author: Tomáš Míčka

@contact: to23mas@gmail.com

@version:  1.0


"""
from django.contrib.auth.models import User, Group
from .models import Exam, Question, Answer, OpenRightAnswer, FailedTest, ExamResult, AviableTest, CompleteTest
from collections import Counter
from django.utils.timezone import now, timedelta, datetime
from lessons.models import Lesson, Chapter
from projects.models import Project


class ExamOverview:
    def __init__(self, user: User):
        """
        Třída es stará o vípisy testů které má uživatel  dispozici a které má již hotové
        @param user: uživatel získaný requestem
        """
        self.user = user


        self.aviable = self.__get_aviable_exams()  # tsty které se dají psát
        self.success = self.__get_completed_exams()  # query set with Exam... úspěšné testy
        self.failed = self.__get_failed_exams() # ne[spesne testy
        self.empty = self.__is_empty()  # pokud nemá nic


    def __get_failed_exams(self):
        """funkce načítá testy, které uživatel pokazil

        @return: None or FailedTest  if found
        """
        failed = FailedTest.objects.filter(user=self.user)

        if failed.exists():
            return failed
        return None

    def __get_aviable_exams(self) -> object:
        """
        hledá dostupné testy

        @return: None or Exam model if found
        """

        aviable = AviableTest.objects.filter(user=self.user)
         # navštívené

        if aviable.exists():

            return aviable
        return None

    def __get_completed_exams(self) -> object:
        """
        hledá a vrací splněné testy

        @return: None or Exam modle query set
        """
        complete = CompleteTest.objects.filter(user=self.user)

        if complete.exists():
            return complete
        return None

    def __is_empty(self) -> bool:
        """funkce hlídá jesli má uživatel vůbec nějaký test dostupnů
        @return: True => pokud uživatel nemá dostupné a splněné žádné testy
        """
        if self.aviable is None and self.success is None and self.failed is None:
            return True
        return False


class Test:
    """třída ptředstavuje samotný test"""
    def __init__(self, user: User, exam_id: id):
        """
        načte test pro odeslání do template

        @param user: uživatel z requestu,
        @param exam_id: číslo testu
        @param exam: test
        @param questions: všechny otázky
        """

        self.exam_id = exam_id
        self.user = user
        self.exam = Exam.objects.get(id=self.exam_id)
        self.questions = Question.objects.filter(exam=self.exam)


class ExamValidation:
    def __init__(self, lesson_id: int, data):
        """
        Validace výsledků testu
        @param lesson_id: číslo testu
        @param data: request.POST
        @param questions: načtení otázek
        @param q_counts: počet otázek
        @param progress: dict s počtem správných a špatných odpovědí
        @param user_answers: seznam odeslaných odpovědí
        @param user_open: otevřená odpověď
        @param retake: jestli se jedná o opakokvaný test
        """

        self.lesson_id = lesson_id
        self.data = data
        self.questions = Question.objects.filter(exam=self.lesson_id)
        self.q_count = self.questions.count()
        self.progress = {}

        self.user_answers = []
        self.user_open = ''

    def __single(self, question: Question):
        """funkce se stará o otázky s jendnou správnou odpovědí
        @param question: příslušná otázka
        """

        # načte id správné odpovědi
        correct = Answer.objects.get(question_id=question, answer_tag='RIGHT').id
        flag = False
        # iterace přes všechny uživatelovy odpovědi
        for answers in self.user_answers:
            if correct == answers:
                flag = True
                break
        if flag:
            self.progress[question.id] = 'RIGHT'
        else:
            self.progress[question.id] = 'WRONG'



    def __multi(self, question: Question):
        """funkce se stará o otázky s více možnými správnými odpověďmi.
        @param question: příslušná otázka
        """
        if len(self.user_answers) == 0:
            self.progress[question.id] = 'WRONG'
            return
        user = self.user_answers
        # načte všechny správné opovědi
        corrects = list(Answer. \
                        objects. \
                        filter(question_id=question, answer_tag='RIGHT'). \
                        values_list('id', flat=True))

        wrongs = list(Answer. \
                      objects. \
                      filter(question_id=question, answer_tag='WRONG'). \
                      values_list('id', flat=True))

        check_correct = all(
            item in list(self.user_answers) for item in corrects)  # true if all correct answers selected
        check_wrong = any(item in wrongs for item in list(self.user_answers))  # true if wrong selected

        if not check_wrong and check_correct:
            self.progress[question.id] = 'RIGHT'
        else:
            self.progress[question.id] = 'WRONG'

    def __check_open(self, question: Question):
        """funkce má na starosti o otázky s otevřenou odpovědí

        @param question: příslušná otázka
        """
        answer = OpenRightAnswer.objects.get(question=question).right_answer

        if str(self.user_open) == answer:
            self.progress[question.id] = 'RIGHT'
        else:
            self.progress[question.id] = 'WRONG'

    def __success(self, user_id: int, percentage, right, wrong):
        """v připadě úspěšně napsaného testu se spouší tato funkce

        @param user_id: id uživatele
        @param percentage: poměr správných a špatných
        @param right: správné odpovědi
        @param wrong: počet špatných
        """
        exam_result = ExamResult.objects.get(exam=self.lesson_id, user_id=user_id)

        exam_result.correct = right
        exam_result.wrong = wrong
        exam_result.percentage = percentage
        exam_result.save()

        #odemknut9 lekce přes group

        next_lesson = Lesson.objects.get(id=self.lesson_id + 1)
        lesson_group = next_lesson.lesson_group
        group = Group.objects.get(name=lesson_group)
        user = User.objects.get(id=user_id)
        user.groups.add(group)
        user.save()

        # odemknutí první kapitoly
        chapter = Chapter.objects.get(chapter_lesson=next_lesson, chapter_order=1)
        chapter.allowed.add(user)

        #splnění testu
        les = Lesson.objects.get(id=self.lesson_id).lesson_order
        exam = Exam.objects.get(exam_number=les)
        complete = CompleteTest.objects.create(user=user, complete_exam=exam)
        complete.save()
        self.__unlock_project(user, self.lesson_id)

        # odstranění dostupneho

        aviable = AviableTest.objects.filter(user=user, aviable_exam=exam)
        if aviable.exists():
            aviable.delete()

        failed = FailedTest.objects.filter(user=user, failed_exam=exam)
        if failed.exists():
            failed.delete()



    def __fail(self, user_id: int, percentage, right, wrong, take=2):
        """v připadě úspěšně napsaného testu se spouší tato funkce

                @param user_id: id uživatele
                @param percentage: poměr správných a špatných
                @param right: správné odpovědi
                @param wrong: počet špatných
                @param take:počet pokusů
                """
        exam_result = ExamResult.objects.get(exam=self.lesson_id, user_id=user_id)
        exam_result.take = take
        exam_result.lock = now() + timedelta(minutes=15)
        exam_result.lock_date = datetime.today()
        exam_result.correct = right
        exam_result.wrong = wrong
        exam_result.percentage = percentage
        exam_result.save()

        user = User.objects.get(id=user_id)
        if take == 2:
            exam = Exam.objects.get(id=self.lesson_id)
            aviable = AviableTest.objects.get(user=user, aviable_exam=exam)
            aviable.delete()
            failed = FailedTest.objects.create(user=user, failed_exam=exam, take=take)
            failed.save()
        elif take == 3:
            exam = Exam.objects.get(id=self.lesson_id)
            failed = FailedTest.objects.get(user=user, failed_exam=exam)
            failed.take = 3
            failed.save()


    def load_data(self):
        """funkce do listu user_answer načte ids jeho odpovědí
            a do user_open načte otevřenou odpověď"""
        for q in self.data:
            print(q)
            if q.isnumeric():

                try:
                    self.user_answers.append(Answer.objects.get(question_id=q, answer_text=self.data[q]).id)
                except:
                    self.user_answers.append(Answer.objects.get(id=q).id)
            elif q == 'OPEN':
                self.user_open = self.data.get('OPEN')

    def validate(self):
        """funkce rozzařuje na menší validace.
        pokud je otázka 'SINGLE' pošle se do funkce určené na spracování tohoto typu otázek"""
        for question in self.questions:

            if question.type_tag == 'SINGLE':
                self.__single(question)
            elif question.type_tag == 'MULTI':
                self.__multi(question)
            elif question.type_tag == 'OPEN':
                self.__check_open(question)

    def result(self, user_id: int):
        """funkce pro výpočet výsledku testu.

        @param user_id: uživatelovo id
        """
        calc_result = Counter(self.progress.values())
        sum = calc_result['RIGHT'] + calc_result['WRONG']
        percentage = calc_result['RIGHT'] / (sum / 100)

        if not ExamResult.objects.filter(exam=self.lesson_id, user_id=user_id).exists():
            ExamResult.objects.create(exam_id=self.lesson_id, user_id=user_id).save()

            if percentage < 60:
                self.__fail(user_id, percentage , calc_result['RIGHT'], calc_result['WRONG'])
            else:
                self.__success(user_id, percentage, calc_result['RIGHT'], calc_result['WRONG'])
        else:
            if percentage < 60:
                self.__fail(user_id, percentage, calc_result['RIGHT'], calc_result['WRONG'], take=3)
            else:
                self.__success(user_id, percentage, calc_result['RIGHT'], calc_result['WRONG'])


    def __unlock_project(self, user: User, id: int)-> None:
        """pro lekce s id nad 2 se odemykají i příslušné testovací projekty"""
        if (id >= 2):
            Project.objects.create(user=user,lesson_id=id+1)
