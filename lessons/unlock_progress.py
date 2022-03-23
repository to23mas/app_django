from django.contrib.auth.models import User

from exams.models import AviableTest, CompleteTest, Exam
from .models import Chapter, Lesson
from lessons.load_data_class import LessonData


class Aviability_Handler:

    @classmethod
    def unlock_lesson(cls, lesson_id: int, user: User) -> None:
        user.groups.add(lesson_id + 1)


    @classmethod
    def unlock_default(cls, user: User) -> None:
        #odemkne první lekci s první kapitolou
        user.groups.add(1)

        chap = Chapter.objects.get(chapter_lesson_id=1, chapter_order=1)
        chap.allowed.add(user)
        chap.save()

    @classmethod
    def unlock_next_chapter(cls, user: User, chapter_order: int, lesson_id: int):
        #existuje další lekce
        next = Chapter.objects.filter(chapter_lesson_id=lesson_id, chapter_order=chapter_order + 1)
        if next.exists():
            # chap = Chapter.objects.get(chapter_lesson_id=lesson_id, chapter_order=chapter_order)
            next.get().allowed.add(user)

            return next.get().chapter_link

        #pokud neexistuje tak odemkni další kapitolu
        cls.unlock_next_lesson(user, lesson_id)

    @classmethod
    def unlock_next_lesson(cls, user: User, lesson_order: int):
        lesson_next = Lesson.objects.get(lesson_order=lesson_order + 1)
        if lesson_next():
            lesson = Lesson.objects.get(lesson_order=lesson_order).complete(user)
            user.groups.add(lesson_next.lesson_group)
            lesson.save()
            user.save()

    @classmethod
    def unlock_chapter_by_reading(csl, user: User, data: LessonData) -> str:

        next_chapter = Chapter.objects.get(chapter_lesson_id=data.lesson.id,
                                           chapter_order=data.chapter.chapter_order + 1).chapter_link

        return next_chapter

    @classmethod
    def unlock_by_text(cls, test: str, user: User, chapter_order: int, lesson_id: int) -> bool:

        if user.username == test:
            return cls.unlock_next_chapter(user, chapter_order=chapter_order, lesson_id=lesson_id)

        return False


    @classmethod
    def unlock_first_test(cls, user: User) -> None:

        exam = Exam.objects.get(exam_header='ÚVODNÍ TEST')

        if AviableTest.objects.filter(user=user, aviable_exam=exam).exists():
            return
        aviable = AviableTest.objects.create(user=user, aviable_exam=exam)

        aviable.save()





