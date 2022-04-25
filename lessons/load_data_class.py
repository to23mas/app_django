"""
Modul s funkcionalitami zídící mi obah jednotlivých učebních textů

classes: LessonData

@author: Tomáš Míčka

@contact: to23mas@gmail.com

@version:  1.0


"""

from lessons.models import Lesson, Chapter, Requirements, Goals
from django.contrib.auth.models import User


class LessonData:
    """třída načítající data v podobě učebních textů k jednotlivým lekcím"""
    def __init__(self, lesson_order: int, chapter_link: str, user: User):
        """konstruktor třídy
        @param lesson: samotná lekce
        @param chapter_link: název kapitoly
        @param chapter: celá Třída zobrazené kapitoly
        @param user: uživatel
        @param chapters: všechny kapitoly patřící k lekci
        @param requirements: požadavky
        @param goals: cíle
        @param chapter_is_complete: true pokud už je kapitola splněna
        """
        self.lesson = self.get_lesson(lesson_order)
        self.chapter_link = chapter_link
        self.chapter = Chapter.objects.get(chapter_lesson_id=self.lesson.id, chapter_link=self.chapter_link)
        self.user = user
        self.chapters = self.get_chapters()
        self.requirements = self.get_requirements()
        self.goals = self.get_goals()
        self.chapter_is_complete = self.is_complete()

    def get_lesson(self, lesson_order: int) -> Lesson:
        """načítá příslušnou lekci"""
        return Lesson.objects.get(lesson_order=lesson_order)

    def get_chapters(self) -> list:
        """načítá k lekci kapitoly"""
        return Chapter.objects.filter(chapter_lesson_id=self.lesson.id).order_by('chapter_order')

    def get_requirements(self) -> list:
        """načítá požadavky k lekci"""
        return Requirements.objects.filter(req_lesson_id=self.lesson.id)

    def get_goals(self) -> list:
        """načítá cíle k lekci"""
        return Goals.objects.filter(goal_lesson_id=self.lesson.id)

    def is_complete(self) -> bool:
        """zjišTúje, jestli je kapitola splněna"""
        if Lesson.objects.filter(id=self.lesson.id, complete=self.user).exists():
            return True
        return False

    def set_chapter(self, chapter: Chapter) -> None:
        """nastavuje novou kapitolu"""
        self.chapter = chapter

    def get_next_chapter(self):
        """načítá následující kapitolu"""
        return Chapter.objects.get(
            chapter_lesson_id=self.lesson.id,
            chapter_order=self.chapter.chapter_order + 1
        )
