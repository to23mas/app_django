from django.contrib.auth.models import User
from .models import Exam, Question, Answer, ExamResult, UserExamProgres, OpenRightAnswer, ExamResult
from collections import Counter
from django.utils.timezone import now, timedelta

class ExamOverview:
    def __init__(self, user: User):
        self.user = user

        self.aviable = self.__get_aviable_exams()
        self.success = self.__get_completed_exams() # query set with Exam
        # self.failed = self.__get_failed()
        # self.failed_once = self.__get_failed_once()
        # self.failed_twice = self.__get_failed_twice()

        self.empty = self.__is_empty()

    def __get_aviable_exams(self):
        aviable = UserExamProgres.objects.get(user=self.user).aviable
        complete = UserExamProgres.objects.get(user=self.user).completed

        result = aviable - complete
        if result == 1:
            return Exam.objects.filter(id=aviable)
        return None

    def __get_completed_exams(self):
        complete = UserExamProgres.objects.get(user=self.user).completed
        complete_ids = list(range(1, complete + 1))

        # TODO test this
        if complete >= 1:
            return Exam.objects.filter(pk__in=complete_ids)

        return None

    def __is_empty(self):
        if self.aviable is None and self.success is None:
            return True
        return False

    # def __get_failed(self):
    #     exam = ExamResult.objects.get(user_id=self.user.id, take=1)
    #     pass
    #
    # def __get_failed_twice(self):
    #     pass


class Test:

    def __init__(self, user: User, exam_id: id):
        self.exam_id = exam_id
        self.user = user
        self.exam = Exam.objects.get(id=self.exam_id)
        self.questions = Question.objects.filter(exam=self.exam)

    def get_questions(self):
        return


class ExamValidation:
    def __init__(self, lesson_id: int, data, retake=False):
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

                exam_result.save()

