from django.db import models


class Lesson(models.Model):
    lesson_name = models.CharField(max_length=200)
    le_sum = models.CharField(max_length=500)
    le_capitols = models.IntegerField()
    le_difficulty = models.IntegerField()


