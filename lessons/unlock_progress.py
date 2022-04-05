from django.contrib.auth.models import User, Group

from exams.models import AviableTest, CompleteTest, FailedTest, Exam
from .models import Chapter, Lesson, TextTest
from lessons.load_data_class import LessonData


class ProgressHandler:

    def __init__(self, user: User, lesson_id: int):
        self.user = user
        self.lesson_id = lesson_id
        self.hint = ''

    def unlock_lesson(self, lesson_id: int, ) -> None:
        self.user.groups.add(lesson_id + 1)


    def unlock_default(self) -> None:
        # odemkne první lekci s první kapitolou

        self.user.groups.add(1)

        chap = Chapter.objects.get(chapter_lesson_id=1, chapter_order=1)
        chap.allowed.add(self.user)
        chap.save()

    def unlock_next_chapter(self, chapter_order: int):
        # existuje další lekce
        next = Chapter.objects.filter(chapter_lesson_id=self.lesson_id, chapter_order=chapter_order + 1)
        if next.exists():
            next.get().allowed.add(self.user)

            return next.get().chapter_link

        # pokud neexistuje tak odemkni další kapitolu
        self.unlock_next_lesson(self.lesson_id)

    def unlock_next_lesson(self, lesson_order: int):
        lesson_next = Lesson.objects.get(lesson_order=lesson_order + 1)
        if lesson_next():
            lesson = Lesson.objects.get(lesson_order=lesson_order).complete(self.user)
            self.user.groups.add(lesson_next.lesson_group)
            lesson.save()
            self.user.save()

    def unlock_chapter_by_reading(self, data: LessonData) -> str:

        next_chapter = Chapter.objects.get(chapter_lesson_id=data.lesson.id,
                                           chapter_order=data.chapter.chapter_order + 1).chapter_link

        return next_chapter

    def unlock_first_by_text(self, test: str, chapter_order: int) -> bool:

        if self.user.username == test:
            return self.unlock_next_chapter(chapter_order=chapter_order)

        return False

    def unlock_first_test(self) -> None:
        exam = Exam.objects.get(exam_header='ÚVODNÍ TEST')
        if self.test_exists(1):
            return

        aviable = AviableTest.objects.create(user=self.user, aviable_exam=exam)
        aviable.save()


    def unlock_test(self):
        exam = Exam.objects.get(exam_number=self.lesson_id)
        if self.test_exists(self.lesson_id):
            return
        aviable = AviableTest.objects.create(user=self.user, aviable_exam=exam)
        aviable.save()


    def unlock_by_text(self, text: str, chapter_order):
        answer = TextTest.objects.get(lesson=self.lesson_id)
        right_answer = answer.text
        users_answer = text
        if right_answer == users_answer:
            return self.unlock_next_chapter(chapter_order=chapter_order)
        self.hint = answer.hint
        return False

    def test_exists(self, lesson_id: int):
        exam = Exam.objects.get(exam_number=lesson_id)
        aviable = AviableTest.objects.filter(user=self.user, aviable_exam=exam)
        if aviable.exists():
            return True
        failed = FailedTest.objects.filter(user=self.user, failed_exam=exam)
        if failed.exists():
            return True

        complete = CompleteTest.objects.filter(user=self.user, complete_exam=exam)
        if complete.exists():
            return True
        return False
