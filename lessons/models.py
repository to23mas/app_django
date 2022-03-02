from django.db import models
from django.contrib.auth.models import User


class Lesson(models.Model):
    lesson_name = models.CharField(max_length=200)
    lesson_group = models.CharField(max_length=30, default='')
    le_short_sum = models.CharField(max_length=500, default='')
    le_long_sum = models.CharField(max_length=10000, default='')
    le_capitols = models.IntegerField()
    le_difficulty = models.IntegerField()

    tags = (
        ("LESSON", 'lekce'),
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
    chapter_order = models.IntegerField(blank=True, null=True)
    chapter_name = models.CharField(max_length=50)
    chapter_link = models.CharField(max_length=25, default='')
    chapter_tag = models.CharField(max_length=10, default="READING", choices=tags)

    allowed = models.ManyToManyField(User)

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


class Content(models.Model):
    content_chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    content_header = models.CharField(max_length=50, default='')
    content_text = models.CharField(max_length=500, default='')

    def __str__(self):
        return str(self.content_chapter) + ' - ' + self.content_header


class Progress(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    lesson01 = models.IntegerField(default=1)
    lesson02 = models.IntegerField(blank=True, null=True)
    lesson03 = models.IntegerField(blank=True, null=True)
    lesson04 = models.IntegerField(blank=True, null=True)
    lesson05 = models.IntegerField(blank=True, null=True)
    lesson06 = models.IntegerField(blank=True, null=True)
    lesson07 = models.IntegerField(blank=True, null=True)
    lesson08 = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.user.username
