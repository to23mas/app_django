from django.contrib.auth.models import User
from .models import Exam, Question, Answer, UserExamProgres, OpenRightAnswer, ExamResult
from collections import Counter
from django.utils.timezone import now, timedelta, datetime


class ExamOverview:
    def __init__(self, user: User):
        """
        Třída es stará o vípisy testů které má uživatel  dispozici a které má již hotové
        @param user: uživatel získaný requestem
        """
        self.user = user


        # TODO test null values -> new user should look into test folder
        self.aviable = self.__get_aviable_exams()  # tsty které se dají psát
        self.success = self.__get_completed_exams()  # query set with Exam... úspěšné testy
        self.empty = self.__is_empty() # pokud nemá nic


    def __get_aviable_exams(self) -> object:
        """
        hledá dostupné testy
        @return: None or Exam model if found
        """
        aviable = UserExamProgres.objects.get(user=self.user).aviable  #dostupné
        complete = UserExamProgres.objects.get(user=self.user).completed #navštívené

        result = aviable - complete  # udává jestli nalezený test je splněn nebo ne
        if result == 1:
            return Exam.objects.filter(id=aviable)
        return None

    def __get_completed_exams(self) -> object:
        """
        hledá a vrací splněné testy
        @return: None or Exam modle query set
        """
        complete = UserExamProgres.objects.get(user=self.user).completed
        complete_ids = list(range(1, complete + 1))

        # TODO test this
        if complete >= 1:
            return Exam.objects.filter(pk__in=complete_ids)
        return None

    def __is_empty(self) -> bool:
        """

        @return: True => pokud uživatel nemá dostupné a splněné žádné testy
        """
        if self.aviable is None and self.success is None:
            return True
        return False


class Test:
    def __init__(self, user: User, exam_id: id):
        """
        načte test pro odeslání do template

        @param user: uživatel z requestu,
        @param exam_id: číslo testu
        """
        self.exam_id = exam_id
        self.user = user
        self.exam = Exam.objects.get(id=self.exam_id)
        self.questions = Question.objects.filter(exam=self.exam)


class ExamValidation:
    def __init__(self, lesson_id: int, data, retake=False):
        """
        Validace výsledků testu
        @param lesson_id: číslo testu
        @param data: request.POST
        @param retake: jestli se jedná o opakokvaný test
        """
        self.retake = retake
        self.lesson_id = lesson_id
        self.data = data
        self.questions = Question.objects.filter(exam=self.lesson_id)
        self.q_count = self.questions.count()
        self.progress = {}

        self.user_answers = []
        self.user_open = ''

    def __single(self, question: Question):

        # načte id správné odpovědi
        correct = Answer.objects.get(question_id=question, answer_tag='RIGHT').id
        flag = False
        # iterace přes všechny uživatelovi odpovědi
        for answers in self.user_answers:
            if correct == answers:
                flag = True
                break
        if flag:
            self.progress[question.id] = 'RIGHT'
        else:
            self.progress[question.id] = 'WRONG'

    def __multi(self, question: Question):
        if len(self.user_answers) == 0:
            self.progress[question.id] = 'WRONG'
            return
        user = self.user_answers
        # načte všechny správné opovědi
        corrects = list(Answer.\
                        objects.\
                        filter(question_id=question, answer_tag='RIGHT').\
                        values_list('id', flat=True))

        wrongs = list(Answer.\
                      objects.\
                      filter(question_id=question, answer_tag='WRONG').\
                      values_list('id', flat=True))

        check_correct = all(
            item in list(self.user_answers) for item in corrects)  # true if all correct answers selected
        check_wrong = any(item in wrongs for item in list(self.user_answers))  # true if wrong selected

        if not check_wrong and check_correct:
            self.progress[question.id] = 'RIGHT'
        else:
            self.progress[question.id] = 'WRONG'

    def __check_open(self, question: Question):
        answer = OpenRightAnswer.objects.get(question=question).right_answer

        if str(self.user_open) == answer:
            self.progress[question.id] = 'RIGHT'
        else:
            self.progress[question.id] = 'WRONG'

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
        for question in self.questions:

            if question.type_tag == 'SINGLE':
                self.__single(question)
            elif question.type_tag == 'MULTI':
                self.__multi(question)
            elif question.type_tag == 'OPEN':
                self.__check_open(question)

    def result(self, user_id: int):
        calc_result = Counter(self.progress.values())
        sum = calc_result['RIGHT'] + calc_result['WRONG']
        percentage = calc_result['RIGHT'] / (sum / 100)
        if not self.retake:
            if not ExamResult.objects.filter(exam=self.lesson_id):
                ExamResult(exam=Exam.objects.get(id=self.lesson_id),
                           user_id=user_id,
                           correct=calc_result['RIGHT'],
                           wrong=calc_result['WRONG'],
                           percentage=percentage).save()
                prog = UserExamProgres.objects.get(user=user_id)
                prog.completed = 1
                prog.save()
            else:
                exam_result = ExamResult.objects.get(exam=self.lesson_id)
                exam_result.take = 2
                exam_result.lock = now() + timedelta(minutes=15)
                exam_result.lock_date = datetime.today()
                exam_result.correct = calc_result['RIGHT']
                exam_result.wrong = calc_result['WRONG']
                exam_result.percentage = percentage
                exam_result.save()
        else:
            if percentage < 60:

                exam_result = ExamResult.objects.get(exam=self.lesson_id)
                exam_result.correct = calc_result['RIGHT']
                exam_result.wrong = calc_result['WRONG']
                exam_result.percentage = percentage
                exam_result.lock = now() + timedelta(minutes=15)
                exam_result.lock_date = datetime.today()

                exam_result.save()

