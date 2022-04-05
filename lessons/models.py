from django.db import models
from django.contrib.auth.models import User



class Lesson(models.Model):
    lesson_name = models.CharField(max_length=200)
    lesson_order = models.IntegerField(blank=True, null=True)
    lesson_group = models.CharField(max_length=30, default='')
    le_short_sum = models.CharField(max_length=500, default='')
    le_long_sum = models.CharField(max_length=10000, default='')
    le_capitols = models.IntegerField()
    le_difficulty = models.IntegerField()

    le_view = models.CharField(max_length=30, blank=True, null=True)

    tags = (
        ("LESSON", 'lekce'),
        ("PROJECT", 'project')
    )


    le_tag = models.CharField(max_length=10, choices=tags, default="LESSON")

    complete = models.ManyToManyField(User, blank=True)

    ordering = ['id']

    def __str__(self):
        return f"lesson - {self.id} - {self.lesson_name}"


class Chapter(models.Model):
    tags = (
        ("READING", 'reading'),
        ("TEXT", "text"),
        ("EXAM", "exam")
    )
    chapter_lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    chapter_order = models.IntegerField(blank=True, null=True)
    chapter_name = models.CharField(max_length=50)
    chapter_link = models.CharField(max_length=25, default='')
    chapter_tag = models.CharField(max_length=10, default="READING", choices=tags)

    allowed = models.ManyToManyField(User, blank=True)

    ordering = ('-chapter_order',)

    def __str__(self):
        return f"lesson: {self.chapter_lesson.id} -- kapitola: {self.chapter_name} -- pořadí: {self.chapter_order}"
        # return self.chapter_lesson.lesson_name + ' - ' + self.chapter_name + ' - ' + str(self.chapter_order)


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
    content_order = models.IntegerField(blank=True, null=True)
    content_header = models.CharField(max_length=50, default='')
    content_text = models.TextField(max_length=1000, default='', blank=True, null=True)
    content_html = models.TextField(max_length=10000, default='', blank=True, null=True)

    ordering = ['content_order']

    def __str__(self):
        return str(self.content_chapter) + ' - ' + str(self.content_order) + ' - ' + self.content_header


class TextTest(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    text = models.TextField(max_length=100, default='', blank=True, null=True)
    hint = models.TextField(max_length=100, default='', blank=True, null=True)

    def __str__(self):
        return str(self.lesson.lesson_name) + ' - ' + self.text
