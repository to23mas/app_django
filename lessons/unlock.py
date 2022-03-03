from django.contrib.auth.models import User
from django.forms import Form

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
    def unlock_chapter_by_reading(user: User, chapter_order: int, lesson_id: int) -> str:
        #nazev nadchazejic9 kapitoly pro redirect TODO pro poslední kapitolu
        next_chapter = Chapter.objects.get(chapter_lesson_id=lesson_id, chapter_order=chapter_order + 1)

        #adding one to progress
        if lesson_id == 1:
            user.progress.lesson01 += 1
            user.progress.save()
            user.save()
        # redirect je potřeba aby uživatel nemohl dotaz poslat znovu a tím si přičíst víc bofů
        return next_chapter

    @staticmethod
    def unlock_by_text(test: str, user: User):

        if user.username == test:
            user.progress.lesson01 += 1
            user.progress.save()
            user.save()
            return True

        return False


class Checker:

    @staticmethod
    def is_chapter_completed(user: User, lesson_id: int, chapter_order: int) -> bool:

        user_progress = 0

        if lesson_id == 1:
            user_progress = user.progress.lesson01  # tabulka progress

        # podm9nka pro hledání, jestli už uživatel lekci splnil
        if chapter_order + 1 <= user_progress:
            return True
        return False
