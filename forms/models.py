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
        
        if Applicant.objects.filter(custom_id=self.custom_id).exclude(pk=self.pk).exists():
            raise ValidationError({"detail": "Duplicate custom_id for user and semester combination."})

        super().save(*args, **kwargs)   


class IntraEventFormSubmission(models.Model):
    event_name = models.CharField(max_length=200)
    segment_name = models.CharField(max_length=200)
    
    team_member_name_1 = models.CharField(max_length=100)
    team_member_student_id_1 = models.CharField(max_length=20)
    is_robu_member_1 = models.BooleanField(default=False)
    robu_dept_1 = models.CharField(max_length=100, blank=True, null=True)
    gsuit_1 = models.CharField(max_length=100, blank=True, null=True)
    
    team_member_name_2 = models.CharField(max_length=100)
    team_member_student_id_2 = models.CharField(max_length=20)
    is_robu_member_2 = models.BooleanField(default=False)
    robu_dept_2 = models.CharField(max_length=100, blank=True, null=True)
    gsuit_2 = models.CharField(max_length=100, blank=True, null=True)

    team_member_name_3 = models.CharField(max_length=100)
    team_member_student_id_3 = models.CharField(max_length=20)
    is_robu_member_3 = models.BooleanField(default=False)
    robu_dept_3 = models.CharField(max_length=100, blank=True, null=True)
    gsuit_3 = models.CharField(max_length=100, blank=True, null=True)

    team_member_name_4 = models.CharField(max_length=100)
    team_member_student_id_4 = models.CharField(max_length=20)
    is_robu_member_4 = models.BooleanField(default=False)
    robu_dept_4 = models.CharField(max_length=100, blank=True, null=True)
    gsuit_4 = models.CharField(max_length=100, blank=True, null=True)

    team_member_name_5 = models.CharField(max_length=100)
    team_member_student_id_5 = models.CharField(max_length=20)
    is_robu_member_5 = models.BooleanField(default=False)
    robu_dept_5 = models.CharField(max_length=100, blank=True, null=True)
    gsuit_5 = models.CharField(max_length=100, blank=True, null=True)

    team_member_name_6 = models.CharField(max_length=100)
    team_member_student_id_6 = models.CharField(max_length=20)
    is_robu_member_6 = models.BooleanField(default=False)
    robu_dept_6 = models.CharField(max_length=100, blank=True, null=True)
    gsuit_6 = models.CharField(max_length=100, blank=True, null=True)

    payment_status = models.CharField(max_length=100)
    transaction_id = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'event_name', 'segment_name'], name='unique_user_event_segment')
        ]

    def save(self, *args, **kwargs):
        existing_submission = IntraEventFormSubmission.objects.filter(
            user=self.user, 
            event_name=self.event_name, 
            segment_name=self.segment_name
        ).exclude(pk=self.pk).first()
        
        if existing_submission:
            raise ValidationError({"detail": "User already has a submission for this event and segment."})

        super().save(*args, **kwargs)
