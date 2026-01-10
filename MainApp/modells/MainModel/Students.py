from django.db import models
from django.core.validators import RegexValidator, EmailValidator
from django.core.exceptions import ValidationError
from datetime import date
from MainApp.modells.Topick.Directions import Direction
from django.utils.translation import gettext_lazy as _

class Applicant(models.Model):
    GENDER_CHOICES = [
        ('M', _('Erkak')),
        ('F', _('Ayol')),
    ]
    education_language = models.CharField(
        max_length=2,
        choices=[('uz', 'Oze'), ('ru', 'Rus'), ('en', 'Eng')],
        default='uz'
    )


    first_name = models.CharField(max_length=50, verbose_name="Ismi")
    last_name = models.CharField(max_length=50, verbose_name="Familiyasi")
    middle_name = models.CharField(max_length=50, blank=True, verbose_name="Otchestvo")
    birth_date = models.DateField(verbose_name="Tug'ilgan sanasi")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name=_("Jinsi"))

    # --- Паспорт и Контакты ---
    passport_regex = RegexValidator(regex=r'^[A-Z]{2}\d{7}$', message="Pasport seriyasi AA1234567 formatida bo'lishi kerak")
    passport_seria = models.CharField(validators=[passport_regex], max_length=9, unique=True, verbose_name="Pasport seriyasi")

    phone_regex = RegexValidator(regex=r'^\+998\d{9}$', message="Tel raqam formati: '+998901234567'.")
    phone_number = models.CharField(validators=[phone_regex], max_length=13, unique=True, verbose_name="Telefon raqami")

    email = models.EmailField(
        unique=True,
        verbose_name="Elektron pochta",
        validators=[EmailValidator(message="To'g'ri email kiriting")]
    )
    address = models.TextField(verbose_name="Yashash manzili")

    parent_first_name = models.CharField(max_length=50, verbose_name="Ota-onasining Ismi")
    parent_last_name = models.CharField(max_length=50, verbose_name="Ota-onasining Familiyasi")
    parent_phone_number = models.CharField(
        validators=[phone_regex],
        max_length=13,
        verbose_name="Ota-onasining Telefoni"
    )

    school_name = models.CharField(max_length=200, verbose_name="Tugatgan maktabi/kolleji")
    is_graduated = models.BooleanField(default=False, verbose_name="Maktabni tugatganmi?")
    direction = models.ForeignKey(Direction, on_delete=models.PROTECT, related_name="applicants", verbose_name="Yo'nalish")

    registration_date = models.DateTimeField(auto_now_add=True, verbose_name="Ro'yxatdan o'tgan vaqti")
    is_approved = models.BooleanField(default=False, verbose_name="Tasdiqlangan")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def clean(self):

        if self.birth_date:
            today = date.today()
            age = today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))
            if age < 18:
                raise ValidationError("Sizning yoshingiz 18 ga to'lmagan.")