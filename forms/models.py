from django.db import models, IntegrityError
from accounts.models import User

class Dept(models.Model):
    choice = models.TextField(null=True, blank=True)
    rank = models.IntegerField(blank=False)
    project = models.ForeignKey('Applicant', on_delete=models.CASCADE, null=True, related_name='applicants')

class Applicant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    about = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=100, blank=False, default='not selected')
    application_date = models.DateField(auto_now_add=True)
    interviewed = models.BooleanField(default=False) 
    dept_choice = models.ManyToManyField(Dept, blank=True) 
    drive_link = models.CharField(max_length=200)
    semester = models.CharField(max_length=100, blank=False, null=False)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'semester'], name='unique_user_semester')
        ]

    def save(self, *args, **kwargs):
        # Check if the combination of user and semester is unique before saving
        if Applicant.objects.filter(user=self.user, semester=self.semester).exists():
            raise IntegrityError("User already has an application for this semester.")
        super().save(*args, **kwargs)