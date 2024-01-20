from django.db import models
from rest_framework.exceptions import ValidationError
from accounts.models import User
from django.utils import timezone

class Applicant(models.Model):
    custom_id = models.CharField(max_length=100, primary_key=True, editable=False, default="")
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    about = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=100, blank=False, null=True)
    application_date = models.DateTimeField(default=timezone.now)
    interview_time = models.DateTimeField(blank=True, null=True)
    interviewed = models.BooleanField(default=False) 
    dept_choice = models.CharField(max_length=200, blank=True, null=True)   
    drive_link = models.CharField(max_length=200, blank=True, null=True)
    semester = models.CharField(max_length=100, blank=False, null=False, default='spring2049')
    assigned_department = models.CharField(max_length=200, blank=True, null=True)
    feedback = models.TextField(null=True, blank=True)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'semester'], name='unique_user_semester')
        ]

    def save(self, *args, **kwargs):
        self.custom_id = f"{self.user.student_id}_{self.semester}"
        # Check if the combination of user and semester is unique before saving
        existing_applicant = Applicant.objects.filter(user=self.user, semester=self.semester).exclude(pk=self.pk).first()
        if existing_applicant:
            raise ValidationError({"detail": "User already has an application for this semester."})

        super().save(*args, **kwargs)