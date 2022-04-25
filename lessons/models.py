"""
Models

model pro aplikaci lessons

classes: Lesson, Chapter, Requirements, Goals, Content, TestText

@author: Tomáš Míčka

@contact: to23mas@gmail.com

@version:  1.0
"""




from django.db import models
from django.contrib.auth.models import User


class Lesson(models.Model):
    """Třída představující Jednotlivé učební lekce.

        @param lesson_name: název lekce
        @param lesson_order: pořadí výpisu ... 1 -> první
        @param lesson_group: skupina, do které musí uživatel patřit, aby mu byla přístupná
        @param le_short_sum: krátký popis
        @param le_long_sum: dlouý popis
        @param le_capitols: počet kapitol
        @param le_difficulty: obtížnost
        @param le_view: Url adresa lekce
        @param le_tag: určuje jaký typ lekce se jedná .... praktická X teoretická
        @param complete: Kteří uživatelé lekci dokončili... OneToMany
        """
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
        """funkce pro výpis -> LESSON - ID - NÁZEV_LEKCE"""
        return f"lesson - {self.id} - {self.lesson_name}"


class Chapter(models.Model):
    """Třída představující kapitoly v lekcích.

        @param chapter_lesson: přiřazená lekce .. cizí klíč
        @param chapter_order: pořadí při vypisování
        @param chapter_name: název kapitoly
        @param chapter_link: url odkaz
        @param chapter_tag: druh lekce
        @param allowed:

    """
    tags = (
        ("READING", 'reading'), # pro splnění kapitoly je potřeba zmáčknout tlačítko
        ("TEXT", "text"), # pro splnění kapitoly je potřeba odpovědět na otázku
        ("EXAM", "exam") # po kliknutí na tlačítko je uživatel přesměrován na test
    )
    chapter_lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    chapter_order = models.IntegerField(blank=True, null=True)
    chapter_name = models.CharField(max_length=50)
    chapter_link = models.CharField(max_length=25, default='')
    chapter_tag = models.CharField(max_length=10, default="READING", choices=tags)

    allowed = models.ManyToManyField(User, blank=True)

    ordering = ('-chapter_order',)

    def __str__(self):
        """funkce pro výpis -> LESSON: ID_LEKCE -- KAPITOLA: NÁZEV KAPITOLY -- POŘADÍ 1"""
        return f"lesson: {self.chapter_lesson.id} -- kapitola: {self.chapter_name} -- pořadí: {self.chapter_order}"


class Requirements(models.Model):
    """Třída představující požadavky na splnění lekceh.

            @param req_lesson: cizí klíč Lekce
            @param requirement: psamotný požadavek

    """
    req_lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    requirement = models.CharField(max_length=500)



class Goals(models.Model):
    """Třída představující ÚČELY jednotlivých lekcí.

        @param goal_lesson: cizí klíč Lekce
        @param goal: cíl lekce

    """
    goal_lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    goal = models.CharField(max_length=500)




class Content(models.Model):
    """Třída představující odstavce u kapitol.

        @param content_chapter: cizí klíč Kapitoly
        @param content_order: pořadí výpisu
        @param content_header: nadpis odstavce
        @param content_text: vlastní text
        @param content_html: text na vypsání s html značkami ...... probýhá escapování znaků
        @param content_dir: adresářová struktura

    """
    content_chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    content_order = models.IntegerField(blank=True, null=True)
    content_header = models.CharField(max_length=50, default='')
    content_text = models.TextField(max_length=2000, default='', blank=True, null=True)
    content_html = models.TextField(max_length=10000, default='', blank=True, null=True)
    content_dir = models.TextField(max_length=1000, default='', blank=True, null=True)

    ordering = ['content_order']

    def __str__(self):
        """funkce pro výpis -> KAPITOLA - POŘADÍ - NADPIS_ODSTAVCE"""
        return str(self.content_chapter) + ' - ' + str(self.content_order) + ' - ' + self.content_header


class TextTest(models.Model):
    """Třída představující otázky pro postup kapitolmi.
        Pokud má kapitola tag === text, bude v ní položena otázka,
        odpovězení na otázku odemyká další kapitoly.

        @param lesson: cizí klíč Lekce
        @param text: otázka
        @param hint: nápověda

    """
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    text = models.TextField(max_length=100, default='', blank=True, null=True)
    hint = models.TextField(max_length=100, default='', blank=True, null=True)

    def __str__(self):
        """funkce pro výpis -> NÁZEV_LEKCE  - OTÁZKA"""
        return str(self.lesson.lesson_name) + ' - ' + self.text
