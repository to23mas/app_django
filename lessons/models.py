from django.db import models


class Lesson(models.Model):
    lesson_name = models.CharField(max_length=200)
    le_short_sum = models.CharField(max_length=500, default='')
    le_long_sum = models.CharField(max_length=10000, default='')
    le_capitols = models.IntegerField()
    le_difficulty = models.IntegerField()

    tags = (
        ("LESSON", 'lesson'),
        ("PROJECT", 'project')
    )

    le_tag = models.CharField(max_length=10, choices=tags, default="LESSON")

    def __str__(self):
        return self.lesson_name


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
