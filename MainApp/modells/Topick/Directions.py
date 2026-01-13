from django.db import models
from django.utils import translation

class Faculty(models.Model):
    name_uz = models.CharField(max_length=200, verbose_name="Fakultet nomi (UZ)")
    name_ru = models.CharField(max_length=200, verbose_name="Название факультета (RU)")
    name_en = models.CharField(max_length=200, verbose_name="Faculty name (EN)")

    @property
    def name(self):
        lang = translation.get_language()
        if lang == 'ru':
            return self.name_ru
        elif lang == 'en':
            return self.name_en
        return self.name_uz

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Факультет"
        verbose_name_plural = "Факультеты"

class Direction(models.Model):
    faculty = models.ForeignKey(
        Faculty,
        on_delete=models.CASCADE,
        related_name='directions',
        verbose_name="Fakultet"
    )

    name_uz = models.CharField(max_length=200, verbose_name="Nomi (UZ)")
    name_ru = models.CharField(max_length=200, verbose_name="Название (RU)")
    name_en = models.CharField(max_length=200, verbose_name="Name (EN)")

    lang_uz = models.BooleanField(default=True, verbose_name="O'zbek guruhi")
    lang_ru = models.BooleanField(default=False, verbose_name="Rus guruhi")
    lang_en = models.BooleanField(default=False, verbose_name="Ingliz guruhi")

    code = models.CharField(max_length=20, unique=True, verbose_name="Yo'nalish kodi")
    quota = models.PositiveIntegerField(verbose_name="Qabul kvotasi")

    @property
    def name(self):
        from django.utils import translation
        lang = translation.get_language()
        if lang == 'ru':
            return self.name_ru
        elif lang == 'en':
            return self.name_en
        return self.name_uz

    def __str__(self):
        return f"{self.code} - {self.name}"

    def get_available_languages(self):
        choices = []
        if self.lang_uz: choices.append(('uz', "O'zbek tili"))
        if self.lang_ru: choices.append(('ru', "Rus tili"))
        if self.lang_en: choices.append(('en', "Ingliz tili"))
        return choices
class Subject(models.Model):
    name = models.CharField(max_length=100, verbose_name="Fan nomi")

    def __str__(self):
        return self.name