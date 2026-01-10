from django.db import models
from MainApp.modells.MainModel.Students import Applicant

class ExamResult(models.Model):
    applicant = models.OneToOneField(Applicant, on_delete=models.CASCADE, related_name="result")
    subject_1_score = models.FloatField(default=0, verbose_name="1-fan bali")
    subject_2_score = models.FloatField(default=0, verbose_name="2-fan bali")
    total_score = models.FloatField(default=0, verbose_name="Umumiy ball")

    def save(self, *args, **kwargs):
        self.total_score = self.subject_1_score + self.subject_2_score
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.applicant} - {self.total_score}"