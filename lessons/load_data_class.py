from lessons.models import Lesson, Chapter, Requirements, Goals, Content
from django.contrib.auth.models import User


class LessonData:

    def __init__(self, lesson_order: int, chapter_link: str, user: User):
        self.lesson = self.get_lesson(lesson_order)

        self.chapter_link = chapter_link

        self.chapter = Chapter.objects.get(chapter_lesson_id=self.lesson.id, chapter_link=self.chapter_link)

        self.user = user
        self.chapters = self.get_chapters()
        self.requirements = self.get_requirements()
        self.goals = self.get_goals()
        self.chapter_is_complete = self.is_complete()

    def get_lesson(self, lesson_order: int) -> Lesson:
        return Lesson.objects.get(lesson_order=lesson_order)

    def get_chapters(self) -> list:
        return Chapter.objects.filter(chapter_lesson_id=self.lesson.id).order_by('chapter_order')

    def get_requirements(self) -> list:
        return Requirements.objects.filter(req_lesson_id=self.lesson.id)

    def get_goals(self) -> list:
        return Goals.objects.filter(goal_lesson_id=self.lesson.id)

    def get_one_chapter(self) -> Chapter:
        pass
        # return Chapter.objects.get(chapter_lesson_id=self.lesson.id, chapter_link=self.chapter_link)

    def is_complete(self) -> bool:
        user_progress = 0

        if Lesson.objects.filter(id=self.lesson.id, complete=self.user).exists():
            return True
        return False
        # return is_chapter_completed(self.user, self.lesson.id, self.chapter.chapter_order)

    def set_chapter(self, chapter: Chapter) -> None:
        self.chapter = chapter

    def get_next_chapter(self):
        return Chapter.objects.get(
            chapter_lesson_id=self.lesson.id,
            chapter_order=self.chapter.chapter_order + 1
        )
