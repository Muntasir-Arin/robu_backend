from django.db import models
from accounts.models import User

class CreatedModel(models.Model):
    name = models.CharField(max_length=255, default='default_table')
    created_at = models.DateTimeField(auto_now_add=True)

class DeptChoice(models.Model):
    name = models.CharField(max_length=255)

class Applicant(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    experience = models.TextField()
    interview_date = models.DateField(null=True, blank=True)
    interview_time = models.TimeField(null=True, blank=True)
    interviewed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student.username}'s Application"

    def save(self, *args, **kwargs):
        table_name = CreatedModel.objects.get(name=self._meta.db_table).name
        Applicant._meta.db_table = table_name
        super(Applicant, self).save(*args, **kwargs)

class Department(models.Model):
    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE)
    choice = models.ForeignKey(DeptChoice, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        your_model_instance = Applicant.objects.first()
        dept_table_name = f"dept_{CreatedModel.objects.get(name=your_model_instance._meta.db_table).created_at.year}"
        DeptChoice._meta.db_table = dept_table_name
        super(Department, self).save(*args, **kwargs)
