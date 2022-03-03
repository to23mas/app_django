from lessons.models import Lesson, Chapter, Requirements, Goals, Content
from django.contrib.auth.models import User
from .unlock import Aviability_Handler, Checker


class LessonData:

    def __init__(self, lesson_id: int, chapter_link: str, user: User):
        self.lesson = self.get_lesson(lesson_id)

        self.chapter_link = chapter_link
        self.chapter = self.get_one_chapter()

        self.user = user
        self.chapters = self.get_chapters()
        self.requirements = self.get_requirements()
        self.goals = self.get_goals()
        self.chapter_is_complete = self.is_complete()

    def get_lesson(self, lesson_id: int) -> Lesson:
        return Lesson.objects.get(id=lesson_id)

    def get_chapters(self) -> list:
        return Chapter.objects.filter(chapter_lesson_id=self.lesson.id).order_by('-id')

    def get_requirements(self) -> list:
        return Requirements.objects.filter(req_lesson_id=self.lesson.id)

    def get_goals(self) -> list:
        return Goals.objects.filter(goal_lesson_id=self.lesson.id)

    def get_one_chapter(self) -> Chapter:
        return Chapter.objects.get(chapter_lesson_id=self.lesson.id, chapter_link=self.chapter_link)

    def is_complete(self):
        return Checker.is_chapter_completed(self.user, self.lesson.id, self.chapter.chapter_order)

    def set_chapter(self, chapter) -> None:
        self.chapter = chapter
