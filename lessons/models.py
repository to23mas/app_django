from django.db import models
from django.contrib.auth.models import User


class Lesson(models.Model):
    lesson_name = models.CharField(max_length=200)
    le_short_sum = models.CharField(max_length=500, default='')
    le_long_sum = models.CharField(max_length=10000, default='')
    le_capitols = models.IntegerField()
    le_difficulty = models.IntegerField()

    allowed = models.ManyToManyField(User)

    tags = (
        ("LESSON", 'lesson'),
        ("PROJECT", 'project')
    )

    le_tag = models.CharField(max_length=10, choices=tags, default="LESSON")

    def __str__(self):
        return self.lesson_name


class Chapter(models.Model):
    tags = (
        ("READING", 'reading'),
        ("TEST", "test"),
        ("EXERCISE", "exercise")
    )
    chapter_lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    chapter_name = models.CharField(max_length=50)
    chapter_link = models.CharField(max_length=25, default='')
    chapter_tag = models.CharField(max_length=10, default="READING", choices=tags)

    users = models.ManyToManyField(User)

    def __str__(self):
        return self.chapter_lesson.lesson_name + ' - ' + self.chapter_name


class Requirements(models.Model):
    req_lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    requirement = models.CharField(max_length=500)

    def __str__(self):
        return self.req_lesson.lesson_name + ' - ' + self.requirement


class Goals(models.Model):
    goal_lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    goal = models.CharField(max_length=500)

    def __str__(self):
        return self.goal_lesson.lesson_name + ' - ' + self.goal


