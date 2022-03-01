from django.contrib.auth.models import User
from .models import  Chapter


class Aviability_Handler:

    @staticmethod
    def unlock_lesson(lesson_id: int, user: User) -> None:
        user.groups.add(lesson_id)

    @staticmethod
    def unlock_default(user: User) -> None:

        user.groups.add(1)
        user.groups.add(2)

        Chapter.objects.get(id=4).allowed.add(user)
        Chapter.objects.get(id=5).allowed.add(user)




    @staticmethod
    def unlock_chapter_by_reading(user: User, previciouse_chapter: str, lesson_id: int) -> str:
        actual_chapter_id = Chapter.objects.get(chapter_lesson_id=lesson_id, chapter_link=previciouse_chapter).id
        actual_chapter_id = + 1

        chapter_for_unclock = Chapter.objects.get(id=actual_chapter_id)
        chapter_for_unclock.allowed.add(user)

        return chapter_for_unclock.chapter_link
