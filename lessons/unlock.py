from django.contrib.auth.models import User
from .models import Lesson, Chapter


class Aviability_Handler:

    @staticmethod
    def unlock_lesson(lesson: Lesson, user: User) -> None:
        lesson.allowed.add(user)

    @staticmethod
    def unlock_default(user: User) -> None:
        lesson_one = Lesson.objects.get(id=1)
        lesson_two = Lesson.objects.get(id=2)

        chapters_one = Chapter.objects.get(id=4)
        chapters_two = Chapter.objects.get(id=5)

        lesson_one.allowed.add(user)
        lesson_two.allowed.add(user)

        chapters_one.allowed.add(user)
        chapters_two.allowed.add(user)


    @staticmethod
    def unlock_chapter_by_reading(user: User, previciouse_chapter: str, lesson_id: int) -> str:
        actual_chapter_id = Chapter.objects.get(chapter_lesson_id=lesson_id, chapter_link=previciouse_chapter).id
        actual_chapter_id = + 1

        chapter_for_unclock = Chapter.objects.get(id=actual_chapter_id)
        chapter_for_unclock.allowed.add(user)

        return chapter_for_unclock.chapter_link
