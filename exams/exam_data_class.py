from django.contrib.auth.models import User
from .models import Exam, Question, Answer, UserExamProgress,OpenRightAnswer


class ExamOverview:
    def __init__(self, user: User):
        self.user = user

        self.aviable = self.get_aviable_exams()
        self.completed = self.get_completed_exams()
        self.empty = self.is_empty()

    def get_aviable_exams(self):
        aviable = UserExamProgress.objects.get(user=self.user).aviable
        complete = UserExamProgress.objects.get(user=self.user).completed

        result = aviable - complete
        if result == 1:
            return Exam.objects.filter(id=aviable)
        return None

    def get_completed_exams(self):
        complete = UserExamProgress.objects.get(user=self.user).completed
        complete_ids = list(range(1, complete + 1))

        # TODO test this
        if complete >= 1:
            return Exam.objects.filter(pk__in=complete_ids)

        return None

    def is_empty(self):
        if self.aviable is None and self.completed is None:
            return True
        return False


class Test:

    def __init__(self, user: User, exam_id: id):
        self.exam_id = exam_id
        self.user = user
        self.exam = Exam.objects.get(id=self.exam_id)
        self.questions = Question.objects.filter(exam=self.exam)

    def get_questions(self):
        return


class ExamValidation:
    def __init__(self, lesson_id: int, data):
        self.lesson_id = lesson_id
        self.data = data
        self.user_answers = []
        self.correct_answers = Answer.objects.filter(exam_id=lesson_id, answer_tag='RIGHT')
        self.correct_open = OpenRightAnswer.objects.get(exam_id=lesson_id)
        self.user_open = ''

    def single(self):
        # data = self.data.
        pass

    def multi(self):
        pass

    def check_open(self, question):
        pass

    def load_data(self):
        for q in self.data:

            if q.isnumeric():
                self.user_answers.append(Answer.objects.get(id=q))

            elif q == 'OPEN':
                self.user_open = self.data.get('OPEN')


    def validate(self):
        list_right = []
        list_user = []
        for a in self.correct_answers:
            list_right.append(a.id)

        for a in self.user_answers:
            list_user.append(a.id)

        if list_right in list_user:
            return True

        else:
            return False
