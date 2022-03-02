from django.contrib.auth.models import User
from .models import Chapter, Progress


class Aviability_Handler:

    @staticmethod
    def unlock_lesson(lesson_id: int, user: User) -> None:
        user.groups.add(lesson_id)

    @staticmethod
    def unlock_default(user: User) -> None:

        user.groups.add(1)
        user.groups.add(2)
        Progress(user=user).save()




    @staticmethod
    def unlock_chapter_by_reading(user: User, current_chapter_name: str, lesson_id: int) -> str:
        # current_chapter_order = Chapter.\
        #     objects.\
        #     get(chapter_link=current_chapter_name, chapter_lesson_id=lesson_id).\
        #     chapter_order

        num = user.progress.lesson01
        num = +1
        user.progress.lesson01 = num
        user.save()

        return ''
