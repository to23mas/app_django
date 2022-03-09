from django.contrib.auth.models import User
from .models import Exam, Question, Answer, UserExamProgress


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
