from django.contrib.auth.models import User

from exams.models import UserExamProgres
from .models import Chapter, Progress
from lessons.load_data_class import LessonData


class Aviability_Handler:

    @staticmethod
    def unlock_lesson(lesson_id: int, user: User) -> None:
        user.groups.add(lesson_id)

    @staticmethod
    def unlock_default(user: User) -> None:
        user.groups.add(1)
        user.groups.add(2)
        UserExamProgres(user=user).save()
        Progress(user=user).save()

    @staticmethod
    def unlock_chapter_by_reading(user: User, data: LessonData) -> str:
        # nazev nadchazejic9 kapitoly pro redirect TODO pro poslední kapitolu
        next_chapter = Chapter.objects.get(chapter_lesson_id=data.lesson.id,
                                           chapter_order=data.chapter.chapter_order + 1).chapter_link
        # adding one to progress
        if data.lesson.id == 1:
            user.progress.lesson01 += 1
            user.progress.save()
            user.save()
        # redirect je potřeba aby uživatel nemohl dotaz poslat znovu a tím si přičíst víc bofů
        return next_chapter

    @staticmethod
    def unlock_by_text(test: str, user: User) -> bool:

        if user.username == test:
            user.progress.lesson01 += 1
            user.progress.save()
            user.save()
            return True
        return False

    @staticmethod
    def lesson_is_completed(user: int, data: int) -> bool:
        if user == data:
            return True
        return False

    @classmethod
    def unlock_first_test(cls, user: User) -> None:
        progress = UserExamProgres.objects.get(user=user)
        if progress.aviable == 0:
            progress.aviable = 1
            progress.save()



